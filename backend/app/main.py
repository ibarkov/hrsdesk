from fastapi import FastAPI
from app.core.database import engine, Base

# Модели
from app.models import product, property  # 👈 добавили property

# Роутеры
from app.routers.products import router as products_router
from app.routers.properties import router as properties_router  # 👈 добавили

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRS Desk API")

@app.get("/")
def root():
    return {"message": "HRS Desk API is running"}

app.include_router(products_router)
app.include_router(properties_router)   # 👈 подключаем роутер отелей
