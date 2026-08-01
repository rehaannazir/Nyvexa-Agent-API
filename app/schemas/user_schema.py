from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    name: str
    email: EmailStr
    passward: str


class UserLogin(BaseModel):
    email: EmailStr
    passward: str


class UserNameUpdate(BaseModel):
    old_username: str
    new_username: str


class UserEmailUpdate(BaseModel):
    old_email: EmailStr
    new_email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
