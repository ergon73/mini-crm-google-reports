"""
Главный файл FastAPI приложения.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.routers import clients, deals, tasks

app = FastAPI(title="Mini-CRM API", version="1.0.0")

# CORS для работы с GUI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключить роутеры
app.include_router(clients.router)
app.include_router(deals.router)
app.include_router(tasks.router)


@app.on_event("startup")
async def startup_event():
    """Инициализация БД при старте."""
    init_db()


@app.get("/health")
def health_check():
    """Проверка здоровья сервиса."""
    return {"status": "ok"}

