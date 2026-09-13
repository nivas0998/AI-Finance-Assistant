
from pydantic import BaseModel, EmailStr
from datetime import date


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TransactionCreate(BaseModel):
    user_id: int
    date: date
    description: str
    amount: float
    type: str
    category: str | None = None


class BudgetCreate(BaseModel):
    user_id: int
    month: str
    category: str
    limit_amount: float
