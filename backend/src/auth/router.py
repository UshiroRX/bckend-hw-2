from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from .schemas import CreateUserRequest, User
from .service import authenticate_user, create_new_user, create_tokens, get_user_from_token, update_access_token, get_user
from .dependencies import db_depends, token_depends, form_depends
from .schemas import Token

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form : form_depends, db : db_depends):
    print(form.username)
    print(form.password)
    user = await authenticate_user(form.username, form.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login or password")
    
    token = create_tokens({"username" : user.username, "role" : "admin"})
    return token

@router.post("/refresh")
async def refresh_access_token(refresh_token : token_depends):
    new_access_token = update_access_token(refresh_token)

    return new_access_token
    


@router.post('/register', response_model=User, status_code=status.HTTP_200_OK)
async def register(form : form_depends, db : db_depends):
    existing_user = await get_user(form.username, db)

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist in system")
    
    new_user = CreateUserRequest(username=form.username, password=form.password)
    result = await create_new_user(new_user, db)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

@router.post('/profile', status_code=status.HTTP_200_OK, response_model=User)
async def get_profile(db: db_depends, current_user : Annotated[str, Depends(get_user_from_token)]):
    return current_user
