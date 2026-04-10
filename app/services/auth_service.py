from fastapi import HTTPException, status
from jose import JWTError, ExpiredSignatureError
from datetime import timedelta
from sqlalchemy.orm import Session
from app.auth.security import create_token, decode_token
from app.utils.db_helpers import get_user_or_404


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def refresh_tokens(self, token: str):
        try:
            payload = decode_token(token)

            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Tipo inválido"
                )

            user_id = payload.get("sub")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
                )

            user = get_user_or_404(self.db, int(user_id))

            access_token = create_token(user.id, "access", timedelta(minutes=15))

            refresh_token = create_token(user.id, "refresh", timedelta(days=7))

            return {"access_token": access_token, "refresh_token": refresh_token}

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado"
            )

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
            )
