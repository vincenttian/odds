import secrets
from jose import JWTError, jwt
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('JWT_SECRET_KEY') # random token url safe secret key 32
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def verify_code(stored_code: str, input_code: str) -> bool:
    return secrets.compare_digest(stored_code, input_code)

def create_verification_code() -> str:
    return secrets.randbelow(1000000).__str__().zfill(6)

async def send_verification_code(phone_number: str, code: str):
    pass
    # async with aiohttp.ClientSession() as session:
    #     payload = {
    #         "to": phone_number,
    #         "message": f"Your verification code is: {code}",
    #         "api_key": SMS_API_KEY
    #     }
    #     async with session.post(SMS_API_URL, json=payload) as response:
    #         if response.status != 200:
    #             raise HTTPException(status_code=500, detail="Failed to send SMS")