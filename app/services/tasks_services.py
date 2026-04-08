from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.tasks_model import Task
from app.models.user_model import User
from app.schemas.tasks_schema import TaskCreate, TaskUpdate
from app.utils.db_helpers import get_task_or_404, check_task_owner


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task_data: TaskCreate, user_id: int):
        new_task = Task(
            description=task_data.description,
            conclued=task_data.conclued,
            user_id=user_id,
        )
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def get_task_id(self, task_id: int, user_id: int):
        task = get_task_or_404(self.db, task_id)
        check_task_owner(task, user_id)

        return task

    def update_task_sv(self, task_id: int, task_data: TaskUpdate, user_id: int):
        task = get_task_or_404(self.db, task_id)
        check_owner = check_task_owner(task_id, user_id)

        if check_owner:
            task_data_up = task_data.model_dump(exclude_unset=True)

            for chave, valor in task_data_up.items():
                if hasattr(task, chave):
                    setattr(task, chave, valor)

            self.db.commit()
            self.db.refresh(task)
            return task

    def delete_task(self, task_id: int, user_id: int):
        task = get_task_or_404(self.db, task_id)
        check_task_owner(task, user_id)

        self.db.delete(task)
        self.db.commit()
        return {"message": "Task deletada com sucesso"}

    def delete_all_tasks(self, confirm: bool, user_id: int):
        if not confirm:
            return {"error": "confirmação necessária"}

        query = select(Task).where(Task.user_id == user_id)
        user_tasks = self.db.execute(query).scalars().all()

        for task in user_tasks:
            self.db.delete(task)

        self.db.commit()
        return {"message": "Todas tasks deletadas com sucesso"}
