from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from db import get_db
from models import User, UserRole
from routes.auth_routes import get_current_user
from schema import PasswordUpdate, UserSchemaIn, UserSchemaOut
from utils import hash_password, verify_password

user_routes = APIRouter()


@user_routes.get("/users/me", response_model=UserSchemaOut)
async def me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@user_routes.post(
    "/users", response_model=UserSchemaOut, status_code=status.HTTP_201_CREATED
)
async def add_user(new_user: UserSchemaIn, sess: Session = Depends(get_db)):
    existing_user = sess.scalar(
        select(User).where(
            or_(User.email == new_user.email, User.username == new_user.username)
        )
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or Email already registered",
        )

    user = User(
        username=new_user.username,
        email=new_user.email,
        password_hash=hash_password(new_user.password),
        role=UserRole.candidate,
    )

    try:
        sess.add(user)
        sess.commit()
        sess.refresh(user)
    except Exception:
        sess.rollback()
        raise
    return user


@user_routes.put("/users/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def password_update(
    password_info: PasswordUpdate,
    current_user: User = Depends(get_current_user),
    sess: Session = Depends(get_db),
):
    if password_info.old_password == password_info.new_password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="old Password & new password is identical",
        )

    if not verify_password(password_info.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Password doesn't match!",
        )
    current_user.password_hash = hash_password(password_info.new_password)
    sess.commit()
    sess.refresh(current_user)
