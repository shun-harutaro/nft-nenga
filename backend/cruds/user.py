from sqlmodel import Session
from models.user import User
from typing import Optional


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: str) -> Optional[User]:
    return db.get(User, user_id)


def update_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> None:
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
