from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

db_depends = Annotated[AsyncSession, Depends(get_session)]

form_depends = Annotated[OAuth2PasswordRequestForm, Depends()]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
token_depends = Annotated[str, Depends(oauth2_scheme)]