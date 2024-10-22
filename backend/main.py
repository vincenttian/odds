import os
from uuid import UUID
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, APIRouter, Body, Depends, HTTPException, Path, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from ariadne import graphql, make_executable_schema, load_schema_from_path, ObjectType
from graphql import GraphQLError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

from models import User, Base
from auth import (
    create_verification_code,
    create_access_token,
    verify_code,
    verify_token,
    SECRET_KEY,
    ALGORITHM
)

# DATABASE_URL="postgresql://vincenttian@localhost:5432/odds_db"
DATABASE_URL = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DATABASE_URL, echo=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)
router = APIRouter(prefix="/api")
security = HTTPBearer()

type_defs = load_schema_from_path("schema.graphql")
query = ObjectType("Query")

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token or expired token")
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_auth(info):
    current_user = info.context["current_user"]
    if not current_user:
        raise GraphQLError("Authentication required")
    return current_user

@query.field("users")
async def resolve_users(_, info):
    # current_user = require_auth(info)
    db = info.context["db"]
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as e:
        print(e)
        raise GraphQLError(f"Database error: {str(e)}")

schema = make_executable_schema(type_defs, [query])

@app.route("/graphql", methods=["GET", "POST"])
async def graphql_route(request: Request):
    if request.method == "GET":
        return JSONResponse({"message": "GraphQL endpoint"})
    elif request.method == "POST":
        async with async_session() as session:
            data = await request.json()
            
            # Get the authorization header
            auth_header = request.headers.get("Authorization")
            current_user = None
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                payload = verify_token(token)
                if payload:
                    user_id = payload.get("sub")
                    if user_id:
                        user = await session.execute(select(User).where(User.id == user_id))
                        current_user = user.scalar_one_or_none()

            success, result = await graphql(
                schema,
                data,
                context_value={"request": request, "db": session, "current_user": current_user},
                debug=app.debug
            )
        return JSONResponse(result, status_code=200 if success else 400)

class PhoneNumber(BaseModel):
    phone: str = Field(..., pattern=r'^\+[1-9]\d{1,14}$')

class VerificationRequest(BaseModel):
    phone: str = Field(..., pattern=r'^\+[1-9]\d{1,14}$')
    code: str = Field(..., min_length=6, max_length=6)

@router.post("/register")
async def register(phone: PhoneNumber, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.phone_number == phone.phone))
    user = user.scalar_one_or_none()
    if user:
        print("User already registered")
        raise HTTPException(status_code=400, detail="User already registered")
    
    code = create_verification_code()
    new_user = User(phone_number=phone.phone, verification_code=code)
    db.add(new_user)
    await db.commit()
    # await send_verification_code(phone.number, code)
    return {"message": "Verification code sent"}

@router.post("/verify")
async def verify(data: VerificationRequest = Body(...), db: AsyncSession = Depends(get_db)):
    phone, code = data.phone, data.code
    user = await db.execute(select(User).where(User.phone_number == phone))
    user = user.scalar_one_or_none()
    if not user:
        print("User not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.verification_code:
        print("No veification code found")
        raise HTTPException(status_code=400, detail="No verification code found")
    
    now = datetime.now(timezone.utc)
    ten_minutes_ago = now - timedelta(minutes=60) # TODO - change back to 10 min
    # Ensure user.verification_code_created_at is timezone-aware
    if user.verification_code_created_at:
        user_code_created_at = user.verification_code_created_at.replace(tzinfo=timezone.utc)
        if user_code_created_at < ten_minutes_ago:
            print("Verification code expired")
            raise HTTPException(status_code=400, detail="Verification code expired")
    
    if not verify_code(user.verification_code, data.code):
        print("Invalid verification code")
        raise HTTPException(status_code=400, detail="Invalid verification code")
    
    user.is_verified = True
    user.phone_verified_at = now
    user.verification_code = None
    user.verification_code_created_at = None
    await db.commit()
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/resend-verification/{user_id}")
async def resend_verification(
    user_id: UUID = Path(..., title="The UUID of the user"),
    db: AsyncSession = Depends(get_db)
):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if enough time has passed since the last code was sent
        if user.verification_code_created_at:
            time_since_last_code = datetime.now(timezone.utc) - user.verification_code_created_at
            if time_since_last_code < timedelta(minutes=1):  # Adjust this time as needed
                raise HTTPException(status_code=429, detail="Please wait before requesting a new code")

        new_code = create_verification_code()
        print("\n\n\n\n\n")
        print(new_code)
        print("\n\n\n\n\n")
        user.verification_code = new_code
        user.verification_code_created_at = datetime.now(timezone.utc)

        db.add(user)
        await db.commit()
        await db.refresh(user)

        # Assume send_verification_code is implemented
        # await send_verification_code(user.phone_number, new_code)

        return {"message": "New verification code sent"}
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login")
async def login(phone: PhoneNumber, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.phone_number == phone.phone))
    user = user.scalar_one_or_none()
    if not user:
        print("USER NOT FOUND")
        raise HTTPException(status_code=400, detail="User not found")

    code = create_verification_code()
    # await send_verification_code(phone.number, code)
    user.verification_code = code
    user.verification_code_created_at = datetime.now(timezone.utc)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "Verification code sent"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    print(f"Invalid request: {exc_str}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc_str}
    )

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5500, log_level="info", reload=True)
