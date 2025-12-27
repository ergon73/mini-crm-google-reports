"""
Роутер для работы с задачами.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlite3 import Connection
from typing import List, Optional
import backend.crud as crud
from backend.database import get_db
from backend.schemas import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=Task, status_code=201)
def create_task(task: TaskCreate, db: Connection = Depends(get_db)):
    """Создать задачу."""
    task_dict = task.model_dump()
    task_id = crud.create_task(db, task_dict)
    created = crud.get_task(db, task_id)
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return created


@router.get("", response_model=List[Task])
def get_tasks(
    q: Optional[str] = Query(None, description="Поиск по названию и описанию"),
    is_done: Optional[bool] = Query(None, description="Фильтр по статусу выполнения"),
    client_id: Optional[int] = Query(None, description="Фильтр по клиенту"),
    deal_id: Optional[int] = Query(None, description="Фильтр по сделке"),
    db: Connection = Depends(get_db)
):
    """Получить список задач."""
    return crud.get_tasks(db, q=q, is_done=is_done, client_id=client_id, deal_id=deal_id)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Connection = Depends(get_db)):
    """Получить задачу по ID."""
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Connection = Depends(get_db)):
    """Обновить задачу."""
    task_dict = task.model_dump(exclude_unset=True)
    if not crud.update_task(db, task_id, task_dict):
        raise HTTPException(status_code=404, detail="Task not found")
    updated = crud.get_task(db, task_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update task")
    return updated


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Connection = Depends(get_db)):
    """Удалить задачу."""
    if not crud.delete_task(db, task_id):
        raise HTTPException(status_code=404, detail="Task not found")

