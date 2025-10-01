from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from backend import schemas, oauth2, models, utils
from backend.database import engine, get_db
from backend.utils import hash, verify

router = APIRouter()

@router.post('/register',response_model=schemas.UserOut)
def userRegister(user: schemas.UserRegister, db:Session=Depends(get_db)):
    existing_user = db.query(models.EcomUser).filter(models.EcomUser.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    #customer_role_id = db.query(models.UserRoles.id).filter(models.UserRoles.role == "customer")

    new_user=models.EcomUser(**user.dict())
    new_user.password=hash(new_user.password)
    db.add(new_user)
    new_user_role=models.UserRoles(username=new_user.username,
        role_id=3)
    db.add(new_user_role)
    db.commit()
    db.refresh(new_user)
    db.refresh(new_user_role)
    return new_user

@router.post('/login',response_model=schemas.Token)
def userLogin(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.EcomUser).filter(models.EcomUser.username == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    access_token = oauth2.create_access_token(data={"user_id": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
