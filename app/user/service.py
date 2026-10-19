from app.user.models.user import User
from sqlalchemy.orm import Session

def get_user(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()
