"""
Скрипт для заполнения БД тестовыми данными.
"""

import argparse
import requests
from faker import Faker
import random
from datetime import datetime, timedelta
from typing import Optional

fake = Faker('ru_RU')


def create_client(base_url: str) -> int:
    """Создать клиента."""
    client = {
        'name': fake.name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'company': fake.company() if random.random() > 0.3 else None,
        'status': random.choice(['active', 'archived'])
    }
    response = requests.post(f"{base_url}/api/clients", json=client)
    response.raise_for_status()
    return response.json()['id']


def create_deal(base_url: str, client_id: Optional[int] = None) -> int:
    """Создать сделку."""
    deal = {
        'title': f"Сделка {fake.word().capitalize()}",
        'amount': round(random.uniform(10000, 1000000), 2),
        'currency': random.choice(['RUB', 'USD', 'EUR']),
        'status': random.choice(['new', 'in_progress', 'closed', 'cancelled']),
        'client_id': client_id if client_id else (random.randint(1, 100) if random.random() > 0.2 else None)
    }
    response = requests.post(f"{base_url}/api/deals", json=deal)
    response.raise_for_status()
    return response.json()['id']


def create_task(base_url: str, client_id: Optional[int] = None, deal_id: Optional[int] = None) -> int:
    """Создать задачу."""
    task = {
        'title': fake.sentence(nb_words=4)[:-1],
        'description': fake.text(max_nb_chars=200) if random.random() > 0.3 else None,
        'due_date': (datetime.now() + timedelta(days=random.randint(-30, 60))).strftime('%Y-%m-%d') if random.random() > 0.3 else None,
        'is_done': random.choice([True, False]),
        'client_id': client_id if client_id else (random.randint(1, 100) if random.random() > 0.3 else None),
        'deal_id': deal_id if deal_id else (random.randint(1, 100) if random.random() > 0.5 else None)
    }
    response = requests.post(f"{base_url}/api/tasks", json=task)
    response.raise_for_status()
    return response.json()['id']


def main():
    parser = argparse.ArgumentParser(description="Заполнить БД тестовыми данными")
    parser.add_argument('--base-url', default='http://localhost:8000', help='URL API')
    parser.add_argument('--n', type=int, default=100, help='Количество записей каждого типа')
    
    args = parser.parse_args()
    
    base_url = args.base_url.rstrip('/')
    
    print(f"Создание {args.n} клиентов...")
    client_ids = []
    for i in range(args.n):
        try:
            client_id = create_client(base_url)
            client_ids.append(client_id)
            if (i + 1) % 10 == 0:
                print(f"  Создано {i + 1}/{args.n} клиентов")
        except Exception as e:
            print(f"  Ошибка при создании клиента {i + 1}: {e}")
    
    print(f"Создание {args.n} сделок...")
    deal_ids = []
    for i in range(args.n):
        try:
            client_id = random.choice(client_ids) if client_ids and random.random() > 0.2 else None
            deal_id = create_deal(base_url, client_id)
            deal_ids.append(deal_id)
            if (i + 1) % 10 == 0:
                print(f"  Создано {i + 1}/{args.n} сделок")
        except Exception as e:
            print(f"  Ошибка при создании сделки {i + 1}: {e}")
    
    print(f"Создание {args.n} задач...")
    for i in range(args.n):
        try:
            client_id = random.choice(client_ids) if client_ids and random.random() > 0.3 else None
            deal_id = random.choice(deal_ids) if deal_ids and random.random() > 0.5 else None
            create_task(base_url, client_id, deal_id)
            if (i + 1) % 10 == 0:
                print(f"  Создано {i + 1}/{args.n} задач")
        except Exception as e:
            print(f"  Ошибка при создании задачи {i + 1}: {e}")
    
    print("Готово!")


if __name__ == "__main__":
    main()

