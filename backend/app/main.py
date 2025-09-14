from fastapi import FastAPI
from app.core.database import engine, Base

# from app.models import product, property, employee, hrs_employee, support_level, duty_roster, ticket

# Создаём таблицы при старте (только для разработки!)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRS Desk API")

@app.get("/")
def root():
    return {"message": "HRS Desk API is running"}
