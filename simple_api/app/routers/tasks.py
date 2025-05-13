from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, crud
from app.database import SessionLocal
from datetime import date
from app.auth import verify_token

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TaskRead)
def create(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(verify_token)
    ):
    return crud.create_task(db, task)

@router.get("/", response_model=List[schemas.TaskRead])
def list_tasks(
    status: Optional[str] = None,
    due_date: Optional[date] = None,
    db: Session = Depends(get_db),
    token: str = Depends(verify_token)
):
    return crud.get_tasks(db, status, due_date)

@router.get("/{task_id}", response_model=schemas.TaskRead)
def read(
    task_id: int, 
    db: Session = Depends(get_db), 
    token: str = Depends(verify_token)
    ):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=schemas.TaskRead)
def update(
    task_id: int, 
    task_data: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(verify_token)
    ):
    task = crud.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
def delete(
    task_id: int, 
    db: Session = Depends(get_db), 
    token: str = Depends(verify_token)
    ):
    task = crud.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}

