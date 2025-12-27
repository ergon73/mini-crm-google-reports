"""
CRUD операции для работы с БД.
"""

import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> Dict[str, Any]:
    """Преобразовать строку в словарь."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


# ===== КЛИЕНТЫ =====

def create_client(conn: sqlite3.Connection, client: dict) -> int:
    """Создать клиента."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (name, email, phone, company, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        client['name'],
        client.get('email'),
        client.get('phone'),
        client.get('company'),
        client.get('status', 'active'),
        datetime.now().isoformat()
    ))
    conn.commit()
    return cursor.lastrowid


def get_clients(
    conn: sqlite3.Connection,
    q: Optional[str] = None,
    status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Получить список клиентов с фильтрацией."""
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    
    query = "SELECT * FROM clients WHERE 1=1"
    params = []
    
    if q:
        query += " AND (name LIKE ? OR email LIKE ? OR phone LIKE ? OR company LIKE ?)"
        search = f"%{q}%"
        params.extend([search] * 4)
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    return cursor.fetchall()


def get_client(conn: sqlite3.Connection, client_id: int) -> Optional[Dict[str, Any]]:
    """Получить клиента по ID."""
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    return cursor.fetchone()


def update_client(conn: sqlite3.Connection, client_id: int, client: dict) -> bool:
    """Обновить клиента."""
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    for key in ['name', 'email', 'phone', 'company', 'status']:
        if key in client and client[key] is not None:
            updates.append(f"{key} = ?")
            params.append(client[key])
    
    if not updates:
        return False
    
    params.append(client_id)
    query = f"UPDATE clients SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    return cursor.rowcount > 0


def delete_client(conn: sqlite3.Connection, client_id: int) -> bool:
    """Удалить клиента."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    return cursor.rowcount > 0


# ===== СДЕЛКИ =====

def create_deal(conn: sqlite3.Connection, deal: dict) -> int:
    """Создать сделку."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO deals (title, amount, currency, status, client_id, close_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        deal['title'],
        deal.get('amount', 0.0),
        deal.get('currency', 'RUB'),
        deal.get('status', 'new'),
        deal.get('client_id'),
        deal.get('close_date'),
        datetime.now().isoformat()
    ))
    conn.commit()
    return cursor.lastrowid


def get_deals(
    conn: sqlite3.Connection,
    q: Optional[str] = None,
    status: Optional[str] = None,
    client_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Получить список сделок с фильтрацией."""
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    
    query = "SELECT * FROM deals WHERE 1=1"
    params = []
    
    if q:
        query += " AND (title LIKE ?)"
        params.append(f"%{q}%")
    
    if status:
        query += " AND status = ?"
        params.append(status)
    
    if client_id:
        query += " AND client_id = ?"
        params.append(client_id)
    
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    return cursor.fetchall()


def get_deal(conn: sqlite3.Connection, deal_id: int) -> Optional[Dict[str, Any]]:
    """Получить сделку по ID."""
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute("SELECT * FROM deals WHERE id = ?", (deal_id,))
    return cursor.fetchone()


def update_deal(conn: sqlite3.Connection, deal_id: int, deal: dict) -> bool:
    """Обновить сделку."""
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    for key in ['title', 'amount', 'currency', 'status', 'client_id', 'close_date']:
        if key in deal and deal[key] is not None:
            updates.append(f"{key} = ?")
            params.append(deal[key])
    
    if not updates:
        return False
    
    params.append(deal_id)
    query = f"UPDATE deals SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    return cursor.rowcount > 0


def delete_deal(conn: sqlite3.Connection, deal_id: int) -> bool:
    """Удалить сделку."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM deals WHERE id = ?", (deal_id,))
    conn.commit()
    return cursor.rowcount > 0


# ===== ЗАДАЧИ =====

def create_task(conn: sqlite3.Connection, task: dict) -> int:
    """Создать задачу."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (title, description, due_date, is_done, client_id, deal_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        task['title'],
        task.get('description'),
        task.get('due_date'),
        1 if task.get('is_done', False) else 0,
        task.get('client_id'),
        task.get('deal_id'),
        datetime.now().isoformat()
    ))
    conn.commit()
    return cursor.lastrowid


def get_tasks(
    conn: sqlite3.Connection,
    q: Optional[str] = None,
    is_done: Optional[bool] = None,
    client_id: Optional[int] = None,
    deal_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    """Получить список задач с фильтрацией."""
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    if q:
        query += " AND (title LIKE ? OR description LIKE ?)"
        search = f"%{q}%"
        params.extend([search, search])
    
    if is_done is not None:
        query += " AND is_done = ?"
        params.append(1 if is_done else 0)
    
    if client_id:
        query += " AND client_id = ?"
        params.append(client_id)
    
    if deal_id:
        query += " AND deal_id = ?"
        params.append(deal_id)
    
    query += " ORDER BY id DESC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Преобразовать is_done из int в bool
    for row in rows:
        row['is_done'] = bool(row['is_done'])
    
    return rows


def get_task(conn: sqlite3.Connection, task_id: int) -> Optional[Dict[str, Any]]:
    """Получить задачу по ID."""
    cursor = conn.cursor()
    cursor.row_factory = dict_factory
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if row:
        row['is_done'] = bool(row['is_done'])
    return row


def update_task(conn: sqlite3.Connection, task_id: int, task: dict) -> bool:
    """Обновить задачу."""
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    for key in ['title', 'description', 'due_date', 'client_id', 'deal_id']:
        if key in task and task[key] is not None:
            updates.append(f"{key} = ?")
            params.append(task[key])
    
    if 'is_done' in task and task['is_done'] is not None:
        updates.append("is_done = ?")
        params.append(1 if task['is_done'] else 0)
    
    if not updates:
        return False
    
    params.append(task_id)
    query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, params)
    conn.commit()
    return cursor.rowcount > 0


def delete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    """Удалить задачу."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cursor.rowcount > 0

