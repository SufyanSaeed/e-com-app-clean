from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, oauth2
from database import get_db

router = APIRouter()

@router.post("/cartAdd")
def addToCart(
    cart_item: schemas.addToCart,
    current_user: models.EcomUser = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(models.Products).filter(models.Products.name == cart_item.name).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{cart_item.name}' not found"
        )
    

    cart_item_check = db.query(models.Cart).filter(
        models.Cart.user_id == current_user.username,
        models.Cart.product_id == product.id
    ).first()

    total_required_qty = cart_item.quantity
    if cart_item_check:
        total_required_qty += cart_item_check.quantity

    if total_required_qty > product.quantity_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.quantity_available} x {product.name} available in stock"
        )
    
    if cart_item_check:
        cart_item_check.quantity += cart_item.quantity
        cart_item_check.total_price = cart_item_check.quantity * product.price
    else:
        new_cart_item = models.Cart(
            user_id=current_user.username,
            product_id=product.id,
            quantity=cart_item.quantity,
            total_price=(product.price)*cart_item.quantity
        )
        db.add(new_cart_item)

    product.quantity_available -= cart_item.quantity
    db.commit()
    return {"message": f"{cart_item.quantity} x {product.name} added to cart"}

@router.delete("/cartRemove/{cart_item_number}")
def removeFromCart(
    cart_item_number: int,
    current_user: models.EcomUser = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    cart_item = db.query(models.Cart).filter(
        models.Cart.id == cart_item_number,
        models.Cart.user_id == current_user.username
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart item with id {cart_item_number} not found"
        )

    # fetch product
    inventory_product = db.query(models.Products).filter(
        models.Products.id == cart_item.product_id
    ).first()

    # delete cart item
    db.delete(cart_item)
    db.commit()

    # restore stock
    if inventory_product:
        inventory_product.quantity_available += cart_item.quantity
        db.commit()

    return {
        "message": f"Cart item for product '{inventory_product.name if inventory_product else cart_item.product_id}' deleted successfully"
    }
    
@router.get("/viewCart")
def viewCart(
    current_user: models.EcomUser = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    user_cart_items=db.query(models.Cart).filter(current_user.username==models.Cart.user_id).all()
    if not user_cart_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart Empty"
        )
    return {"cart_items":user_cart_items}


