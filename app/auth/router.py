from app.auth.schema.register_schema import RegisterSchema
from app.auth.schemas import LoginRequest
from app.user.service import get_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.auth import service
from app.core.db import get_db
from app.core.security import verify_password, create_access_token
from app.auth.schemas import Token

router = APIRouter()

@router.post("/register-account")
def register_user(payload: RegisterSchema, db: Session = Depends(get_db)):

    result = service.register_user(db=db, payload=payload)

    return result

@router.post("/login", response_model=Token)
def login(
    payload: LoginRequest, db: Session = Depends(get_db)
):
    user = get_user(db=db, email=payload.email)
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer",
             'user_details': {'id': user.id, 'name': user.name, 'email': user.email}}
