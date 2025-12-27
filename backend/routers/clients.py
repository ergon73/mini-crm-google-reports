"""
Роутер для работы с клиентами.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlite3 import Connection
from typing import List, Optional
import backend.crud as crud
from backend.database import get_db
from backend.schemas import Client, ClientCreate, ClientUpdate

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.post("", response_model=Client, status_code=201)
def create_client(client: ClientCreate, db: Connection = Depends(get_db)):
    """Создать клиента."""
    client_dict = client.model_dump()
    client_id = crud.create_client(db, client_dict)
    created = crud.get_client(db, client_id)
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create client")
    return created


@router.get("", response_model=List[Client])
def get_clients(
    q: Optional[str] = Query(None, description="Поиск по имени, email, телефону, компании"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    db: Connection = Depends(get_db)
):
    """Получить список клиентов."""
    return crud.get_clients(db, q=q, status=status)


@router.get("/{client_id}", response_model=Client)
def get_client(client_id: int, db: Connection = Depends(get_db)):
    """Получить клиента по ID."""
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}", response_model=Client)
def update_client(client_id: int, client: ClientUpdate, db: Connection = Depends(get_db)):
    """Обновить клиента."""
    client_dict = client.model_dump(exclude_unset=True)
    if not crud.update_client(db, client_id, client_dict):
        raise HTTPException(status_code=404, detail="Client not found")
    updated = crud.get_client(db, client_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update client")
    return updated


@router.delete("/{client_id}", status_code=204)
def delete_client(client_id: int, db: Connection = Depends(get_db)):
    """Удалить клиента."""
    if not crud.delete_client(db, client_id):
        raise HTTPException(status_code=404, detail="Client not found")

