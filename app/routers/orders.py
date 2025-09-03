from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session, joinedload
from ..DataBase import get_db
from .. import models
from ..schemas import CreateOrder, ResToOrders
from typing import List



router = APIRouter(
                    prefix = "/orders",
                    tags =['orders']
                    )



@router.post("/create",response_model = ResToOrders)
def create_orders(order: CreateOrder, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == order.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {order.user_id} not found")

    new_order = models.Order(user_id=order.user_id)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/get",response_model = List[ResToOrders])
def get_orders(db:Session = Depends(get_db)):
    all_orders = db.query(models.Order).options(joinedload(models.Order.order_items).joinedload(models.OrderItems.product)).all()
    return all_orders



@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_orders(id: int, db:Session = Depends(get_db)):
    order_query = db.query(models.Order).filter(models.Order.id == id)
    order_to_delete = order_query.first()
    if order_to_delete is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = "Not found")

    order_query.delete(synchronize_session=False)
    db.commit()
    return 





"""i guess, the update option is not suitable for orders, it's best to create and delete orders than updating"""
# @router.put("/update/{id}",response_model = ResToOrders)
# def update_orders(id:int,db:Session = Depends(get_db)):
#     exists = db.query(models.Order).filter(models.Order.id == id).first()
#     if exists is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="not found in the DB")

#     update_data = product.model_dump(exclude_unset=True)
#     db.add(product_to_update)
#     db.commit()
#     db.refresh(product_to_update)
#     return product_to_update