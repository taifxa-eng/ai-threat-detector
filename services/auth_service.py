import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Request, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config.settings import settings
from models.base import get_db
from models.user import User

logger = logging.getLogger("auth_service")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ================= PASSWORD =================
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# ================= TOKEN =================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# ================= AUTH =================
def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


# ================= CREATE ADMIN =================
def create_admin_user() -> None:
    from models.base import SessionLocal
    db = SessionLocal()
    try:
        if settings.ADMIN_USERNAME and settings.ADMIN_PASSWORD:
            existing = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
            if not existing:
                new_user = User(
                    username=settings.ADMIN_USERNAME,
                    hashed_password=hash_password(settings.ADMIN_PASSWORD),
                    is_admin=True,
                )
                db.add(new_user)
                db.commit()
                logger.info("Admin created")
    except Exception as exc:
        logger.error(f"Admin error: {exc}")
    finally:
        db.close()


# ================= CURRENT USER =================
def get_current_user(request: Request, db: Session = Depends(get_db)):

    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user