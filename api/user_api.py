from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from db import get_db
from models import User, UserRole
from schema import PasswordUpdate, UserSchemaIn, UserSchemaOut
from utils import hash_password, verify_password

user_routes = APIRouter()


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


@user_routes.get(
    "/users", status_code=status.HTTP_200_OK, response_model=list[UserSchemaOut]
)
async def get_users(sess: Session = Depends(get_db)):
    return sess.scalars(select(User)).all()


@user_routes.get(
    "/users/{user_id}", response_model=UserSchemaOut, status_code=status.HTTP_200_OK
)
async def get_user(user_id: int, sess: Session = Depends(get_db)):
    user = sess.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )
    return user


@user_routes.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(user_id: int, sess: Session = Depends(get_db)):
    user_exists = sess.get(User, user_id)
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user doesn't exists",
        )
    sess.delete(user_exists)
    sess.commit()


@user_routes.put("/users/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
async def password_update(
    user_id: int, password_info: PasswordUpdate, sess: Session = Depends(get_db)
):

    if password_info.old_password == password_info.new_password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="old Password & new password is identical",
        )

    user_exists = sess.get(User, user_id)
    if user_exists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user doesn't exists",
        )
    if not verify_password(password_info.old_password, user_exists.password_hash):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Password doesn't match!",
        )
    user_exists.password_hash = hash_password(password_info.new_password)
    sess.commit()
    sess.refresh(user_exists)
