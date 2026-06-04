from datetime import UTC, datetime, timedelta
from os import getenv
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import get_db
from models import User
from schema import TokenResponse
from utils import create_access_token, decode_access_token, verify_password

auth_routes = APIRouter()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/login")

JWT_KEY: str | None = getenv("JWT_SECRET")
if JWT_KEY is None:
    raise ValueError("Jwt secret not loaded!")


@auth_routes.post("/login", response_model=TokenResponse)
async def verify_user(
    user_info: OAuth2PasswordRequestForm = Depends(), sess: Session = Depends(get_db)
) -> TokenResponse:
    user_exists = sess.scalar(select(User).where(User.email == user_info.username))

    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials",
        )
    if not verify_password(user_info.password, user_exists.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials!",
        )

    expire = datetime.now(UTC) + timedelta(minutes=30)
    payload: dict[str, str | datetime] = {
        "sub": str(user_exists.user_id),
        "role": user_exists.role.value,
        "exp": expire,
    }
    token = create_access_token(payload)

    return TokenResponse(access_token=token)


async def get_current_user(
    token: str = Depends(oauth2_schema), sess: Session = Depends(get_db)
) -> User:
    try:
        payload: dict[str, Any] = decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_exists = sess.get(User, int(user_id))
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user_exists
