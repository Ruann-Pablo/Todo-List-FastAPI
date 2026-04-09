from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.security import decode_access_token
from app.models.user_model import User
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    payload = decode_access_token(token)

    user_id = payload.get("sub")

    query = select(User).where(User.id == user_id)
    user = db.execute(query).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado"
        )

    return user
