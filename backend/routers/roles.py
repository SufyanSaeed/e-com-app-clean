from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import schemas, models, oauth2
from backend.database import get_db

router = APIRouter()

@router.post("/roles")
def addRole(
    role:schemas.Role,
    current_user: models.EcomUser = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)    
):
    new_role=models.Roles(
        role=role.role
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return {"message": f"{new_role.role} role has been created"}

@router.put("/changeRoleToAdmin/{username}")
def change_role_to_admin(username:str,db:Session=Depends(get_db)):
    user_check=db.query(models.UserRoles).filter(models.UserRoles.username==username).first()
    if not user_check:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username does not exist"
        )
    
    user_check.role_id=2
    db.commit()
    db.refresh(user_check)
    return {"message": f"User {username} role changed to admin"}

@router.get("/is_admin/{username}")
def is_admin(username: str, db: Session = Depends(get_db)):
    user = db.query(models.EcomUser).filter(models.EcomUser.username == username).first()
    if not user:
        return {"is_admin": False}

    user_role = db.query(models.UserRoles).filter(models.UserRoles.username== user.username).first()
    
    # assume role_id 2 = admin
    return {"is_admin": user_role.role_id == 2}








