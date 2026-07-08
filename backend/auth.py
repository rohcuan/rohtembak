import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

class TokenData(BaseModel):
    username: str
    subscription_expiry: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        subscription_expiry: str = payload.get("subscription_expiry")
        if username is None or subscription_expiry is None:
            return None
        return TokenData(username=username, subscription_expiry=subscription_expiry)
    except JWTError:
        return None

def check_subscription_expired(expiry_str: str) -> bool:
    """Check if subscription has expired"""
    try:
        expiry_date = datetime.strptime(expiry_str, "%d-%m-%Y")
        return expiry_date < datetime.now()
    except ValueError:
        return True
