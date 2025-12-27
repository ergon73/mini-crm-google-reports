"""
Роутер для работы со сделками.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlite3 import Connection
from typing import List, Optional
import backend.crud as crud
from backend.database import get_db
from backend.schemas import Deal, DealCreate, DealUpdate

router = APIRouter(prefix="/api/deals", tags=["deals"])


@router.post("", response_model=Deal, status_code=201)
def create_deal(deal: DealCreate, db: Connection = Depends(get_db)):
    """Создать сделку."""
    deal_dict = deal.model_dump()
    deal_id = crud.create_deal(db, deal_dict)
    created = crud.get_deal(db, deal_id)
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create deal")
    return created


@router.get("", response_model=List[Deal])
def get_deals(
    q: Optional[str] = Query(None, description="Поиск по названию"),
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    client_id: Optional[int] = Query(None, description="Фильтр по клиенту"),
    db: Connection = Depends(get_db)
):
    """Получить список сделок."""
    return crud.get_deals(db, q=q, status=status, client_id=client_id)


@router.get("/{deal_id}", response_model=Deal)
def get_deal(deal_id: int, db: Connection = Depends(get_db)):
    """Получить сделку по ID."""
    deal = crud.get_deal(db, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


@router.put("/{deal_id}", response_model=Deal)
def update_deal(deal_id: int, deal: DealUpdate, db: Connection = Depends(get_db)):
    """Обновить сделку."""
    deal_dict = deal.model_dump(exclude_unset=True)
    if not crud.update_deal(db, deal_id, deal_dict):
        raise HTTPException(status_code=404, detail="Deal not found")
    updated = crud.get_deal(db, deal_id)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update deal")
    return updated


@router.delete("/{deal_id}", status_code=204)
def delete_deal(deal_id: int, db: Connection = Depends(get_db)):
    """Удалить сделку."""
    if not crud.delete_deal(db, deal_id):
        raise HTTPException(status_code=404, detail="Deal not found")

