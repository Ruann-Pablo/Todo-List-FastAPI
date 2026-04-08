from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.tasks_model import Task
from app.models.user_model import User


def get_user_or_404(db: Session, user_id: int):
    query = select(User).where(User.id == user_id)
    user = db.execute(query).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )

    return user


def get_task_or_404(db: Session, task_id: int):
    query = select(Task).where(Task.id == task_id)
    task = db.execute(query).scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task não encontrada"
        )

    return task


def check_task_owner(task, user_id: int):
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado"
        )
