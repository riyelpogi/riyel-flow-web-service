from datetime import datetime, timedelta
import bcrypt
from jose import jwt

def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password."""
    try:
        # Handle both string and bytes hash formats
        if isinstance(hashed_password, str):
            hashed_bytes = hashed_password.encode('utf-8')
        else:
            hashed_bytes = hashed_password
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_bytes)
    except Exception as e:
        # Log error but don't expose details
        print(f"Password verification error: {str(e)}")
        return False

def get_password_hash(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode("utf-8")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "fallback_secret", algorithm="HS256")
    return encoded_jwt
