from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Users
from .utils import hash_password, verify_password
from .schemas import CreateUserRequest, Token, User, UserInDB
import jwt
from jwt.exceptions import InvalidTokenError
from .dependencies import db_depends, token_depends
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_DAYS = 7


async def get_user_from_token(token: token_depends, db : db_depends) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            return None
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
  
    user = await get_user(username, db)

    return User.model_validate(user)
    

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode["exp"] = expire


    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def create_tokens(data: dict) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_token(data, access_token_expires)
    refresh_token = create_token(data, refresh_token_expires)  

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

def update_access_token(refresh_token: str):
    payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
    new_access_token = create_token({"username" : payload["username"], "role" : payload["role"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return new_access_token

async def get_user(username: str, db : AsyncSession) -> UserInDB:
    query = select(Users).where(Users.username == username)
    result = await db.execute(query)
    user = result.scalars().first()

    if user is None:
        return None

    return UserInDB.model_validate(user)

async def create_new_user(request : CreateUserRequest, db : AsyncSession) -> User:
    new_user = Users(
        username=request.username,
        hashed_password=hash_password(request.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return User.model_validate(new_user)

async def authenticate_user(username: str, password: str, db : AsyncSession) -> User:
    user = await get_user(username, db)
    if user is None:  
        return None  

    if not verify_password(password, user.hashed_password):  
        return None  

    return User.model_validate(user)
