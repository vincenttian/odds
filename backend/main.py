from fastapi import FastAPI, APIRouter, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from ariadne import graphql, make_executable_schema, load_schema_from_path, ObjectType
from pydantic import BaseModel, Field

# from ariadne.constants import PLAYGROUND_HTML
from models import User, Base
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from starlette.responses import JSONResponse
from auth import create_verification_code, create_access_token
import uvicorn

DATABASE_URL = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DATABASE_URL, echo=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)
router = APIRouter(prefix="/api")

type_defs = load_schema_from_path("schema.graphql")
query = ObjectType("Query")

@query.field("users")
async def resolve_users(_, info):
    async_session = sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            # return {"users": users}
            return users
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

schema = make_executable_schema(type_defs, [query])

@app.route("/graphql", methods=["GET", "POST"])
async def graphql_route(request):
    if request.method == "GET":
        # Handle GET requests (e.g., for GraphQL Playground)
        return JSONResponse({"message": "GraphQL endpoint"})
    elif request.method == "POST":
        data = await request.json()
        success, result = await graphql(
            schema,
            data,
            context_value={"request": request},
            debug=app.debug
        )
        return JSONResponse(result, status_code=200 if success else 400)

class PhoneNumber(BaseModel):
    phone: str = Field(..., pattern=r'^\+[1-9]\d{1,14}$')

class VerificationRequest(BaseModel):
    phone: str = Field(..., pattern=r'^\+[1-9]\d{1,14}$')
    code: str = Field(..., min_length=6, max_length=6)

@router.post("/register")
async def register(phone: PhoneNumber):
    # user = await User.get_by_phone(phone.number)
    # if user:
    #     raise HTTPException(status_code=400, detail="User already registered")
    
    code = create_verification_code()
    # await send_verification_code(phone.number, code)
    # await User.create(phone=phone.number, verification_code=code)
    return {"message": "Verification code sent"}

@router.post("/verify")
async def verify(data: VerificationRequest = Body(...)):
    phone, code = data.phone, data.code
    # user = await User.get_by_phone(phone.number)
    # if not user or user.verification_code != code.code:
    #     raise HTTPException(status_code=400, detail="Invalid code")
    
    # user.is_verified = True
    # await user.save()
    
    access_token = create_access_token(data={"sub": str("user.id")})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
async def login(phone: PhoneNumber):
    # user = await User.get_by_phone(phone.number)
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    
    code = create_verification_code()
    # await send_verification_code(phone.number, code)
    # user.verification_code = code
    # await user.save()
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
