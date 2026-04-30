from datetime import timedelta, timezone, datetime
from typing import Annotated
from database import sessionLocal
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import Users
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import jwt , JWTError



# User registers → password hashed → stored in DB
#
# User logs in → password checked → JWT token created
#
# User sends token → token verified → user fetched

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
SECRET_KEY = "8fcbf7a33fc3872b31ec7805f25895918599de2020f17183870308e4b8dd4a6a"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class createUserRequest(BaseModel):
    username : str
    email : str
    first_name : str
    last_name : str
    password : str
    role : str
    phone_number : str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = sessionLocal() 
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def create_access_token(username : str, user_id : int, role : str, expires_delta : timedelta):
    encode = {'sub':username, 'id' : user_id, 'role' : role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires })
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token :Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        username: str = payload['sub']
        user_id: int = payload['id']
        user_role: str = payload['role']

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return { 'username': username, 'id': user_id, 'role': user_role }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

def authenticate_user(username : str, password : str , db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db : db_dependency, userRequest : createUserRequest):
    tmpUserModel = Users(
        username = userRequest.username,
        email = userRequest.email,
        first_name = userRequest.first_name,
        last_name = userRequest.last_name,
        role = userRequest.role,
        hashed_password = bcrypt_context.hash(userRequest.password),
        is_active = True,
        phone_number = userRequest.phone_number
    )
    db.add(tmpUserModel)
    db.commit()

@router.post("/token")
async def login_access_token(given_input : Annotated[OAuth2PasswordRequestForm, Depends()], db : db_dependency):
    user = authenticate_user(given_input.username, given_input.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}
