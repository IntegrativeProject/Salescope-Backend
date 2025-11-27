from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..models.users import User
from ..models.roles import Role
from ..schemas.users import UserCreate, UserUpdate


def _get_role_id_by_name(db: Session, role_name: str) -> Optional[int]:
    role = db.query(Role).filter(Role.role_name == role_name).first()
    return role.role_id if role else None


def create_user(db: Session, data: UserCreate) -> Optional[User]:
    role_id = _get_role_id_by_name(db, data.role_name)
    if role_id is None:
        return None
    user = User(
        full_name=data.full_name,
        email=data.email,
        role_id=role_id,
        password_hash=data.password_hash,
        is_active=data.is_active if data.is_active is not None else True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int) -> Optional[User]:
    return (
        db.query(User)
        .filter(
            User.user_id == user_id,
            User.is_active == True,
            User.deleted_at.is_(None),
        )
        .first()
    )


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return (
        db.query(User)
        .filter(
            User.email == email,
            User.is_active == True,
            User.deleted_at.is_(None),
        )
        .first()
    )


def list_users(db: Session, skip: int = 0, limit: int = 50) -> List[User]:
    return (
        db.query(User)
        .filter(User.is_active == True, User.deleted_at.is_(None))
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_user(db: Session, user_id: int, data: UserUpdate) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None

    if data.full_name is not None:
        user.full_name = data.full_name
    if data.email is not None:
        user.email = data.email
    if data.role_name is not None:
        role_id = _get_role_id_by_name(db, data.role_name)
        if role_id is None:
            return None
        user.role_id = role_id
    if data.password_hash is not None:
        user.password_hash = data.password_hash
    if data.is_active is not None:
        user.is_active = data.is_active

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    user.is_active = False
    user.deleted_at = func.now()
    # deleted_by can be set later from auth context
    db.add(user)
    db.commit()
    db.refresh(user)
    return True
