from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from models import Todos, Users
from database import sessionLocal
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class userVerification(BaseModel):
    password : str
    new_password : str = Field(min_length=4)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user :user_dependency, db : db_dependency ):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(user: user_dependency, db : db_dependency , user_verification : userVerification):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    # verify if the password is correct
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException (status_code=401, detail="Incorrect password")
    # change the password
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put("/phonenumber/{phonenumber}", status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user : user_dependency, db : db_dependency, phonenumber : str):
    if user is None :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phonenumber
    db.add(user_model)
    db.commit()