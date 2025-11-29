from datetime import datetime, timedelta, timezone
from typing import Optional, Any, Dict

from jose import jwt
from passlib.context import CryptContext
from os import getenv

# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],  # bcrypt_sha256 safely handles long passwords
    deprecated="auto",
)


def hash_password(password: str) -> str:
    # Force bcrypt_sha256 for new hashes to avoid bcrypt 72-byte limit
    return pwd_context.hash(password, scheme="bcrypt_sha256")


def verify_password(plain_password: str, password_hash: str) -> bool:
    try:
        return pwd_context.verify(plain_password, password_hash)
    except ValueError:
        # For legacy bcrypt hashes: retry with 72-byte truncation
        try:
            truncated = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
            return pwd_context.verify(truncated, password_hash)
        except Exception:
            return False


# JWT
SECRET_KEY = getenv("SECRET_KEY", "change-me")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
