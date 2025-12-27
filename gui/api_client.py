"""
Клиент для работы с API.
"""

import requests
from typing import List, Dict, Optional


class APIClient:
    """Клиент для работы с FastAPI backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        """GET запрос."""
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    
    def _post(self, endpoint: str, data: Dict) -> Dict:
        """POST запрос."""
        response = requests.post(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    
    def _put(self, endpoint: str, item_id: int, data: Dict) -> Dict:
        """PUT запрос."""
        response = requests.put(f"{self.base_url}{endpoint}/{item_id}", json=data)
        response.raise_for_status()
        return response.json()
    
    def _delete(self, endpoint: str, item_id: int):
        """DELETE запрос."""
        response = requests.delete(f"{self.base_url}{endpoint}/{item_id}")
        response.raise_for_status()
    
    # Клиенты
    def get_clients(self, q: Optional[str] = None, status: Optional[str] = None) -> List[Dict]:
        """Получить список клиентов."""
        params = {}
        if q:
            params['q'] = q
        if status:
            params['status'] = status
        return self._get("/api/clients", params)
    
    def get_client(self, client_id: int) -> Dict:
        """Получить клиента по ID."""
        response = requests.get(f"{self.base_url}/api/clients/{client_id}")
        response.raise_for_status()
        return response.json()
    
    def create_client(self, client: Dict) -> Dict:
        """Создать клиента."""
        return self._post("/api/clients", client)
    
    def update_client(self, client_id: int, client: Dict) -> Dict:
        """Обновить клиента."""
        return self._put("/api/clients", client_id, client)
    
    def delete_client(self, client_id: int):
        """Удалить клиента."""
        self._delete("/api/clients", client_id)
    
    # Сделки
    def get_deals(self, q: Optional[str] = None, status: Optional[str] = None, client_id: Optional[int] = None) -> List[Dict]:
        """Получить список сделок."""
        params = {}
        if q:
            params['q'] = q
        if status:
            params['status'] = status
        if client_id:
            params['client_id'] = client_id
        return self._get("/api/deals", params)
    
    def get_deal(self, deal_id: int) -> Dict:
        """Получить сделку по ID."""
        response = requests.get(f"{self.base_url}/api/deals/{deal_id}")
        response.raise_for_status()
        return response.json()
    
    def create_deal(self, deal: Dict) -> Dict:
        """Создать сделку."""
        return self._post("/api/deals", deal)
    
    def update_deal(self, deal_id: int, deal: Dict) -> Dict:
        """Обновить сделку."""
        return self._put("/api/deals", deal_id, deal)
    
    def delete_deal(self, deal_id: int):
        """Удалить сделку."""
        self._delete("/api/deals", deal_id)
    
    # Задачи
    def get_tasks(self, q: Optional[str] = None, is_done: Optional[bool] = None, client_id: Optional[int] = None, deal_id: Optional[int] = None) -> List[Dict]:
        """Получить список задач."""
        params = {}
        if q:
            params['q'] = q
        if is_done is not None:
            params['is_done'] = is_done
        if client_id:
            params['client_id'] = client_id
        if deal_id:
            params['deal_id'] = deal_id
        return self._get("/api/tasks", params)
    
    def get_task(self, task_id: int) -> Dict:
        """Получить задачу по ID."""
        response = requests.get(f"{self.base_url}/api/tasks/{task_id}")
        response.raise_for_status()
        return response.json()
    
    def create_task(self, task: Dict) -> Dict:
        """Создать задачу."""
        return self._post("/api/tasks", task)
    
    def update_task(self, task_id: int, task: Dict) -> Dict:
        """Обновить задачу."""
        return self._put("/api/tasks", task_id, task)
    
    def delete_task(self, task_id: int):
        """Удалить задачу."""
        self._delete("/api/tasks", task_id)

