from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..DataBase import get_db
from .. import models, schemas, token
from .. import hashing
from typing import List
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
                   )


@router.post("/create", response_model=schemas.ResToUser)
def create_user(user: schemas.CreateUser,db:Session  = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.email == user.email).first()
    if exists:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials, Already Exists, So Please Go to Login Page")  
    hashed_password = hashing.hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not hashing.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    access_token = token.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/get",response_model = List[schemas.ResToUser])
def get_users(db:Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users



@router.delete("/delete/{id}")
def delete_user(id, db:Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.id == id).first()
    if exists:
        db.delete(exists)
        db.commit()
        return f"hey, now it's no more,. like your EX left you 😂😂😂"
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                        detail = "Check the details and Re-Enter, I can feel that you got Dementia 😂😂😂")