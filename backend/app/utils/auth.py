from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict

from jose import jwt
from passlib.context import CryptContext
from os import getenv

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],  # bcrypt_sha256 safely handles long passwords
    deprecated="auto"
)

def hash_password(password: str) -> str:
    # Let passlib handle the rounds automatically
    return pwd_context.hash(password, scheme="bcrypt_sha256")

def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        # Try to verify the password
        if pwd_context.verify(plain_password, password_hash):
            return True
            
        # If that fails, try with 72-byte truncation for legacy hashes
        truncated = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
        return pwd_context.verify(truncated, password_hash)
    except (ValueError, Exception):
        return False

# JWT configuration
SECRET_KEY = getenv("SECRET_KEY", "change-me")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)