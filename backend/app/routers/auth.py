from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.database import get_db
from app.core import config
from app.models.property_employee import PropertyEmployee
from app.models.hrs_employee import HrsEmployee

router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # проверяем сначала среди HRS сотрудников
    user = db.query(HrsEmployee).filter(HrsEmployee.email == form_data.username).first()
    role = "hrs"
    if not user:
        # потом ищем среди сотрудников отелей
        user = db.query(PropertyEmployee).filter(PropertyEmployee.email == form_data.username).first()
        role = "property"
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if isinstance(user, HrsEmployee) and user.is_admin:
        role = "admin"

    access_token = create_access_token(data={"sub": str(user.id), "role": role})
    return {"access_token": access_token, "token_type": "bearer"}
