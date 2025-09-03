from fastapi import APIRouter,Depends,HTTPException,status,Response
from sqlalchemy.orm import Session
from ..DataBase import get_db
from .. import models
from ..schemas import CreateProduct,ResToProducts
from typing import List



router = APIRouter(
    prefix  = "/products",
    tags = ["products"]
    )




@router.post("/create")
def create_product(product:CreateProduct, db:Session = Depends(get_db)):
    exists = db.query(models.Products).filter(models.Products.name == product.name).first()
    if exists is  None:
        payload  = product.model_dump()
        add= models.Products(**payload)
        db.add(add)
        db.commit()
    else:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= "gottchu, already exists in the DB")
    

@router.get("/get", response_model = List[ResToProducts])
def get_products( db:Session = Depends(get_db)):
    all_products=  db.query(models.Products).all()
    return all_products




@router.put("/update/{id}")
def update_products(id: int, product: CreateProduct, db: Session = Depends(get_db)):
    product_to_update = db.query(models.Products).filter(models.Products.id == id).first()

    if product_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="not found in the DB")

    update_data = product.model_dump(exclude_unset=True)
    db.add(product_to_update)
    db.commit()
    db.refresh(product_to_update)
    return product_to_update



@router.delete("/delete/{id}",status_code = 204)
def delete_products(id:int,db:Session = Depends(get_db)):
    exists = db.query(models.Products).filter(models.Products.id == id)
    product_to_delete = exists.first()
    if exists is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = "Not Found, Please Enter Right Details to Delete a Product")
    exists.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)



