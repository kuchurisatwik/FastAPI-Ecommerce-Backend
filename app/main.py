from fastapi  import FastAPI,Depends,HTTPException, status
from .schemas import CreateUser,ResToUser
from .DataBase import engine,get_db
from . import models 
from sqlalchemy.orm import Session
from typing import List
from .routers  import users,products,orders,order_items,payments


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title = "Ecom-app",
    description = "on your own"
)

@app.get("/")
def check():
    return "it's working"



app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(order_items.router)
app.include_router(payments.router)







     