from pydantic import BaseModel,EmailStr
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password:str


class UserRegister(UserLogin):
    
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email:EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None

class ProductBase(BaseModel):
    name: str
    price: float
    quantity_available: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True

#cart-----------------------------------------------------
class addToCart(BaseModel):
    name:str
    quantity:int

class removeFromCart(BaseModel):
    name:str

class Role(BaseModel):
    role:str