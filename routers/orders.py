from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, oauth2
from database import get_db

router = APIRouter()

@router.get("/checkout") 
def checkout(
    current_user: models.EcomUser = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    user_cart_items=db.query(models.Cart).filter(current_user.username==models.Cart.user_id).all()
    if not user_cart_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cart Empty"
        )
    price=0
    order_items = []
    for cart_item in user_cart_items:
        price+=cart_item.total_price 
        order_items.append({
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "price": cart_item.total_price
        })

    new_order = models.Order(
            user_id=current_user.username,
            total_bill=price,
            items=order_items
    )
    db.add(new_order)
    for cart_item in user_cart_items:
        db.delete(cart_item)
    db.commit()
    db.refresh(new_order)
    return new_order
