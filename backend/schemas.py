"""
Pydantic схемы для валидации данных.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Клиенты
class ClientBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: str = "active"


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None


class Client(ClientBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True


# Сделки
class DealBase(BaseModel):
    title: str
    amount: float = 0.0
    currency: str = "RUB"
    status: str = "new"
    client_id: Optional[int] = None
    close_date: Optional[str] = None


class DealCreate(DealBase):
    pass


class DealUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    client_id: Optional[int] = None
    close_date: Optional[str] = None


class Deal(DealBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True


# Задачи
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    is_done: bool = False
    client_id: Optional[int] = None
    deal_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    is_done: Optional[bool] = None
    client_id: Optional[int] = None
    deal_id: Optional[int] = None


class Task(TaskBase):
    id: int
    created_at: str
    
    class Config:
        from_attributes = True

