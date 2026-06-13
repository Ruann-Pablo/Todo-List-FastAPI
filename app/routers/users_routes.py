from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.users_services import UserService
from app.services.auth_service import AuthService
from app.auth.security import create_token, decode_token
from datetime import timedelta
from app.schemas.users_schema import (
    CreateUser,
    LoginUser,
    UserUpdate,
    UserResponse,
    CreateUserResponse,
    UpdateUserResponse,
)
from app.auth.dependicies import get_current_user, security

router = APIRouter(prefix="/user", tags=["Users"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateUserResponse,
)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    service = UserService(db)
    new_user = service.create_user(user)

    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_datas: LoginUser, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.auth_user(user_datas)

    access_token = create_token(user.id, type_token="access")
    refresh_token = create_token(
        user.id, type_token="refresh", time_token=timedelta(days=7)
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_me(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = UserService(db)
    user = service.get_user_by_id_service(current_user.id)
    return user


@router.patch("/me", status_code=status.HTTP_200_OK, response_model=UpdateUserResponse)
def update_user(
    data_user: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = UserService(db)
    user = service.update_user_service(current_user.id, data_user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service = UserService(db)
    user = service.delete_user_service(current_user.id)
    return {"message": "Usuário deletado com sucesso."}


@router.post("/refresh")
def use_refresh_token(token: str = Depends(security), db: Session = Depends(get_db)):
    service = AuthService(db)
    payload = service.refresh_tokens(token)
    return payload
