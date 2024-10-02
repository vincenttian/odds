from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import User, Base
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import uvicorn

from db import (
    insertItem,
)

DATABASE_URL = os.environ["DATABASE_URL"]

app = FastAPI()

# Add this block after creating the FastAPI app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_users():
    # return {"Status": True, "Version": "1.3.6", "sportsday": True}
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        users = session.query(User).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.commit()
        session.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5500, log_level="info", reload=True)
