from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_details: dict


class LoginRequest(BaseModel):
    email: str
    password: str
