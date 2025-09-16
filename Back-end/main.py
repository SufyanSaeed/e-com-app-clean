from fastapi import FastAPI,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
import schemas,oauth2
import models,utils
from typing import List
from database import engine,get_db
from sqlalchemy.orm import Session
from routers import auth, roles, products, cart, orders
from utils import hash,verify
from typing import List
from fastapi.middleware.cors import CORSMiddleware

#-----------------------------
app = FastAPI()
origins=["https://www.google.com"]
app.add_middleware(
  CORSMiddleware,
  allow_origins = origins,
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers=["*"]
)
app.include_router(auth.router)
app.include_router(roles.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)

models.Base.metadata.create_all(bind=engine)


#creating a dependency







    
#---------------ENDPOINTS FOR USER REGISTER/LOGIN---------------------


@app.get('/')
def hello():
    return {"message":"success api"}





#------------ ECOM PRODUCTS RELATED QUERIES-----------------------------------




#---------------------- CART FUNCITONALITY HAPPENING HERE --------------------------------------------------#
#-------------------------------------------ROLE RELATED END POINTS-------------------------------------  
