from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
import models, schemas, oauth2
from database import get_db
from permissions import admin_required  

router = APIRouter()

@router.get("/ecomProducts", response_model=List[schemas.Product])
def get_all_products(
    db: Session = Depends(get_db),
    current_user: models.EcomUser = Depends(oauth2.get_current_user)
):
    products = db.query(models.Products).all()
    return products


@router.post("/addProducts",response_model=schemas.Product)
def addProducts(
    product: schemas.ProductCreate,
    current_user: models.EcomUser = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
    _: None = Depends(admin_required)
):
    new_product = models.Products(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/ecomProducts/{id}",response_model=schemas.Product)
def getProducts(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)
                ):

    prod_query = db.query(models.Products).filter(models.Products.id == id)
    prod = prod_query.first()    
    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Product with id {id} not found"
        )
    return prod

@router.delete("/ecomProducts/{id}")
def delete_product(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.EcomUser = Depends(oauth2.get_current_user),
    _: None = Depends(admin_required)
):
    prod_query = db.query(models.Products).filter(models.Products.id == id)
    prod = prod_query.first()

    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )

    prod_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Product was successfully deleted"}

@router.put("/ecomProducts/{id}", response_model=schemas.Product)
def update_product(
    id: int,
    updated_prod: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.EcomUser = Depends(oauth2.get_current_user),
    _: None = Depends(admin_required)
):
    prod_query = db.query(models.Products).filter(models.Products.id == id)
    prod = prod_query.first()

    if not prod:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {id} not found"
        )

    prod_query.update(updated_prod.dict(), synchronize_session=False)
    db.commit()
    db.refresh(prod)

    return prod
