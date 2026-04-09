from fastapi import HTTPException, status
from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.core.config import settings

pwd_context = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(
    user_id: int, time_token=timedelta(minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES)
):
    data_expiracao = datetime.now(timezone.utc) + time_token
    payload = {"sub": user_id, "exp": data_expiracao}
    encoded_token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
