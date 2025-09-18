from fastapi import FastAPI
from app.core.database import engine, Base

# Модели
from app.models import product, property, property_employee

# Роутеры
from app.routers.products import router as products_router
from app.routers.properties import router as properties_router
from app.routers.property_employees import router as property_employees_router
from app.routers.hrs_employees import router as hrs_employees_router
from app.routers.auth import router as auth_router


# Создание таблиц при старте (только для разработки!)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRS Desk API")

@app.get("/")
def root():
    return {"message": "HRS Desk API is running"}

# Подключаем роутеры
app.include_router(products_router)
app.include_router(properties_router)
app.include_router(property_employees_router)
app.include_router(hrs_employees_router)
app.include_router(auth_router)
