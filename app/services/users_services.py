from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.user_model import User
from app.schemas.users_schema import CreateUser, UserUpdate, LoginUser
from app.auth.security import hash_password, verify_password
from app.utils.db_helpers import get_user_or_404


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: CreateUser):
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hash_password(user_data.password),
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def auth_user(self, user_data: LoginUser):
        query = select(User).where(User.email == user_data.email)
        user = self.db.execute(query).scalars().first()

        if not user or not verify_password(user_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
            )

        return user

    def get_user_by_id_service(self, user_id: int):
        user = get_user_or_404(self.db, user_id)
        return user

    def update_user_service(self, user_id: int, user_data_up: UserUpdate):
        user = get_user_or_404(self.db, user_id)

        update_datas = user_data_up.model_dump(exclude_unset=True)

        for field, value in update_datas.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)

        return user

    def delete_user_service(self, user_id: int):
        user = get_user_or_404(self.db, user_id)

        self.db.delete(user)
        self.db.commit()

        return True
