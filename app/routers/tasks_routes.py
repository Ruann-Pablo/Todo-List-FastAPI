from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.services.tasks_services import TaskService
from app.auth.dependicies import get_current_user
from app.schemas.tasks_schema import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    CreateTaskResponse,
    UpdateTaskResponse,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CreateTaskResponse
)
def create_tasks_router(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = TaskService(db)
    new_task = service.create_task(task, current_user.id)
    return new_task


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def get_task_by_id(
    task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    service = TaskService(db)

    response_task = service.get_task_id(task_id, current_user.id)
    return response_task


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[TaskResponse],
)
def get_task_by_title(task_title: str, db: Session = Depends(get_db)):
    service = TaskService(db)
    response_task = service.get_task_title(task_title)

    return response_task


@router.patch(
    "/{task_id}", status_code=status.HTTP_200_OK, response_model=UpdateTaskResponse
)
def update_task(
    task_id: int,
    data_task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = TaskService(db)

    task_updated = service.update_task_sv(task_id, data_task, current_user.id)
    return task_updated


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task_by_id(
    task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    service = TaskService(db)
    task_deleted = service.delete_task(task_id, current_user.id)
    return {"message": "Task deletada com sucesso"}


@router.delete("/", status_code=status.HTTP_200_OK)
def delete_all_tasks(
    confirm: bool = False,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service = TaskService(db)
    tasks_deleteds = service.delete_all_tasks(confirm, current_user.id)

    return {"message": "Todas tasks deletadas com sucesso"}
