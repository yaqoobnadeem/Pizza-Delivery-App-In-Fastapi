from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import SignupModel, LoginModel
from models import User
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db_session():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignupModel, db: Session = Depends(get_db_session)):
    db_email = db.query(User).filter(User.email == user.email).first()
    
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    db_username = db.query(User).filter(User.username == user.username).first()
    
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(username=user.username, email=user.email, password=hashed_password, is_staff=user.is_staff, is_active=user.is_active)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.user_id}

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db_session)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if db_user and pwd_context.verify(user.password, db_user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        
        return jsonable_encoder({"access": access_token, "refresh": refresh_token})
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Username or Password")
