from enum import Enum
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from notificationSender import send_message
from db import (
    insertItem,
)

import os

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

class itemTypes(Enum):
    ANNOUNCEMENTS = "announcements"
    EVENTS = "events"


class teamColors(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    NONE = "none"


class user(BaseModel):
    deviceID: str
    name: str
    teamColor: teamColors
    pushToken: str = None
    gpa: float = None

# @app.get("/")
# def get():
#     return {"Status": True, "Version": "1.3.6", "sportsday": True}

@app.get("/")
def get_users():
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

@app.post("/pushNotification/")
async def push(token: str, title: str, message: str, itemType: itemTypes):
    if itemType == itemTypes.ANNOUNCEMENTS:
        page = {"Link": "MainTab/News"}
    elif itemType == itemTypes.EVENTS:
        page = {"Link": "MainTab/Team Color"}
    else:
        page = None
    send_message(token, title, message, data=page)
    return "Success"


@app.post("/pushNotificationAll/")
async def pushall(title: str, message: str, itemType: itemTypes):
    if itemType == itemTypes.ANNOUNCEMENTS:
        page = {"Link": "MainTab/News"}
    elif itemType == itemTypes.EVENTS:
        page = {"Link": "MainTab/Team Color"}
    else:
        page = None
    for pushTokens in splitArr(listPushTokens(), 10):
        send_message(pushTokens, title, message, data=page)
    return "Success"



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5500, log_level="info", reload=True)
