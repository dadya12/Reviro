from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional
from datetime import date

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_tasks(db: Session, status: Optional[str] = None, due_date: Optional[date] = None) -> List[models.Task]:
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    if due_date:
        query = query.filter(models.Task.due_date == due_date)
    return query.all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def update_task(db: Session, task_id: int, task_data: schemas.TaskCreate):
    task = get_task(db, task_id)
    if task:
        for key, value in task_data.dict().items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
    return task
