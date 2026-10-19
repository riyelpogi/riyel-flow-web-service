
from app.auth.schema.register_schema import RegisterSchema
from app.user.models.user import User
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.security import get_password_hash


def register_user(payload: RegisterSchema, db: Session):
    try:
        existing_user = db.query(User).filter(User.email == payload.email).first()

        if existing_user != None:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "sucess": False,
                    "message": "Email is already registered."
                }
            )
        password_hash = get_password_hash(payload.password)
        user = User(
            name=payload.name,
            email=payload.email,
            password_hash=password_hash,
        )
        db.add(user)
        db.flush()

        db.commit()
        return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "sucess": True,
                    'user': {'name': user.name, 'email': user.email, 'id': user.id},
                    "message": "Account successfuly created."
                }
            ) 

    except Exception as err:
        print(err)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(err)
        )
