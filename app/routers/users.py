from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..DataBase import get_db
from .. import models
from ..schemas import CreateUser,ResToUser
from typing import List

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
                   )


@router.post("/create")
def create_user(user: CreateUser,db:Session  = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials, Already Exists, So Please Go to Login Page")  
    payload = user.model_dump()
    newuser = db.add(models.User(**payload))
    db.commit()
    return payload



@router.get("/get",response_model = List[ResToUser])
def get_users(db:Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users



@router.delete("/delete/{id}")
def delete_user(id, db:Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.id == id).first()
    if exists:
        db.delete(exists)
        db.commit()
        return f"hey, now it's no more, like your EX left you 😂😂😂"
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Check the details and Re-Enter, I can feel that you got Dementia 😂😂😂")