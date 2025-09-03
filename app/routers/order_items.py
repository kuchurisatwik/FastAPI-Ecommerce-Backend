from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..DataBase import get_db
from .. import models
from ..schemas import CreateOrderItems,ResOrderItems,DeleteOrderItems
from typing import List



router  = APIRouter(
    prefix = "/orderitems",
    tags = ['items','order_items']
)


@router.post("/create",response_model = ResOrderItems)
def create_order_items(items:CreateOrderItems,db:Session = Depends(get_db)):
    exists = db.query(models.Order).filter(models.Order.id == items.order_id).first()
    if exists is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"order_id with id: {items.order_id} is not found in the DB, please place an order or enter the order_id correctly to add items in specfic order ")
    
    product = db.query(models.Products).filter(models.Products.id == items.product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {items.product_id} not found")

    order_item = models.OrderItems(
        order_id=items.order_id,
        product_id=items.product_id,
        quantity=items.quantity,
        price=product.price
    )
    
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item
        
                            

@router.get("/get",response_model = List[ResOrderItems])
def get_order_items(db:Session = Depends(get_db)):
    get_all_items = db.query(models.OrderItems).all()
    return get_all_items



@router.put("/update/{orderitem_id}",response_model = ResOrderItems)
def update_order_items(orderitem_id: int,items:CreateOrderItems,db:Session = Depends(get_db)):
    # CHECK
    exists = db.query(models.OrderItems).filter(models.OrderItems.order_id == items.order_id , models.OrderItems.id == orderitem_id)
    order_items_db = exists.first()
    if order_items_db is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"the orderitem_id: {orderitem_id} or order_id: {items.order_id} is not found, please cross check it are create orderitems within a order to update.")
    
    product = db.query(models.Products).filter(models.Products.id == items.product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {items.product_id} not found")

    update_data = items.model_dump(exclude_unset=True)
    if 'price' not in update_data:
        update_data['price'] = product.price

    exists.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(order_items_db)
    return order_items_db





@router.delete("/delete/{orderitem_id}", status_code=204)
def delete_orders(orderitem_id: int, items: DeleteOrderItems, db: Session = Depends(get_db)):
    order_item_to_delete = db.query(models.OrderItems).filter(
        models.OrderItems.id == orderitem_id,
        models.OrderItems.order_id == items.order_id
    ).first()
    if order_item_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order item with id {orderitem_id} and order_id {items.order_id} not found"
        )
    product = db.query(models.Products).filter(models.Products.id == items.product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {items.product_id} not found"
        )
    db.delete(order_item_to_delete)
    db.commit()



# @router.delete("/delete/{orderitem_id}",status_code= 204)
# def delete_orders(orderitem_id: int,items:DeleteOrderItems, db:Session = Depends(get_db)):
#     exists = db.query(models.OrderItems).filter(models.OrderItems.id == orderitem_id,models.OrderItems.order_id == items.order_id)
#     order_item_to_delete = exists.first()
#     product = db.query(models.Products).filter(models.Products.id == items.product_id).first()
#     if product is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {items.product_id} not found")
#     if order_item_to_delete:
#         exists.delete(synchronize_session = False)
#         db.commit()
#     else:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "Not found")