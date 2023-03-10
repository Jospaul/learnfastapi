import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from .auth import get_current_user, get_user_exception, get_password_hash, token_exception, verify_password, authenticate_user

class UpdateUser(BaseModel):
    username: str
    password: str
    new_password: str

class UpdatePhoneNumber(BaseModel):
    phone_number: str

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401: {"description": "Not Authorized"}}
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()

@router.get("/{user_id}")
async def get_by_user_id(user_id: int, db: Session = Depends(get_db)):
    user_model =  db.query(models.Users)\
                    .filter(models.Users.id == user_id)\
                    .first()
    if user_model is not None:
        return user_model
    raise user_not_found()

@router.get("/user/")
async def get_user_by_query_id(user_id: int, db: Session = Depends(get_db)):
    user_model =  db.query(models.Users)\
                    .filter(models.Users.id == user_id)\
                    .first()
    if user_model is not None:
        return user_model
    raise user_not_found()

@router.patch("/update_password")
async def update_user_password(new_password: UpdateUser,
                               user: dict = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    
    if user is None:
        raise get_user_exception
    users_model = db.query(models.Users)\
                    .filter(models.Users.id == user.get("id"))\
                    .first()
    if users_model is not None:
        if new_password.username == users_model.username and verify_password(
            new_password.password, users_model.hashed_password):
            users_model.hashed_password = get_password_hash(new_password.new_password)
            db.add(users_model)
            db.commit()
        else:
            raise token_exception()
    else:
        raise user_not_found()


    return successful_response(200)

@router.patch("/update_phone_number/")
async def update_phone_number(phonenumber: UpdatePhoneNumber, user: dict = Depends(get_current_user), 
                              db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    users_model = db.query(models.Users)\
                    .filter(models.Users.id == user.get("id"))\
                    .first()
    if users_model is not None:
        users_model.phone_number = phonenumber.phone_number
        db.add(users_model)
        db.commit()
    else:
        raise user_not_found()
    
    return successful_response(200)
    
@router.delete("/delete_user")
async def delete_user(user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    users_model = db.query(models.Users)\
                    .filter(models.Users.id == user.get("id"))\
                    .first()
    if users_model is None:
        raise user_not_found()
    
    db.delete(users_model)
    db.commit()

    return successful_response(200)

def user_not_found():
    return HTTPException(
        status_code=404, 
        detail = "User not found"
    )

def successful_response(status_code: int):
    return {
        'status': status_code,
        'transaction': 'Successful'
    }