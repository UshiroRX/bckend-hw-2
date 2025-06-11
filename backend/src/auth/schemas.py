from pydantic import BaseModel, ConfigDict


class CreateUserRequest(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

