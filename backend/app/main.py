from fastapi import FastAPI
from app.core.database import engine, Base

# Регистрируем модели, чтобы Base видел таблицы
from app.models import product  # noqa: F401

from app.routers.products import router as products_router

# Создание таблиц при старте (только для DEV!)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRS Desk API")

@app.get("/")
def root():
    return {"message": "HRS Desk API is running"}

app.include_router(products_router)
