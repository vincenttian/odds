from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import graphql, make_executable_schema, load_schema_from_path, ObjectType

# from ariadne.constants import PLAYGROUND_HTML
from models import User, Base
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
import uvicorn

DATABASE_URL = os.environ["DATABASE_URL"].replace("postgresql://", "postgresql+asyncpg://")
engine = create_async_engine(DATABASE_URL, echo=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

type_defs = load_schema_from_path("schema.graphql")
query = ObjectType("Query")

@query.field("users")
async def resolve_users(_, info):
    async_session = sessionmaker(engine, class_=AsyncSession)
    async with async_session() as session:
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            return {"users": users}
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))

schema = make_executable_schema(type_defs, [query])

@app.get("/graphql")
async def graphql_route(request):
    data = await request.json()
    success, result = await graphql(
        schema,
        data,
        context_value={"request": request},
        debug=app.debug
    )
    return JSONResponse(result, status_code=200 if success else 400)

# @app.get("/graphql/playground")
# async def graphql_playground():
#     return PLAYGROUND_HTML

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5500, log_level="info", reload=True)
