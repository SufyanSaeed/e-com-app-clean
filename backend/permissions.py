from fastapi import FastAPI,HTTPException,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from backend import schemas,oauth2
from backend import models,utils
from typing import List
from backend.database import engine,get_db
from sqlalchemy.orm import Session
from backend.utils import hash,verify
from typing import List


def admin_required(current_user = Depends(oauth2.get_current_user),db: Session = Depends(get_db)):
  user = db.query(models.EcomUser).filter(models.EcomUser.username == current_user.username).first()
  
  userrole = db.query(models.UserRoles).filter(models.UserRoles.username == user.username).first()
  
  role = db.query(models.Roles).filter(models.Roles.id == userrole.role_id).first()
  if role.role != "admin":
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
  return True