from fastapi import APIRouter, HTTPException, status
from database import Session, engine
from schemas import SignupModel
from models import User
from passlib.context import CryptContext

auth_router = APIRouter()

session = Session(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@auth_router.post("/signup" , response_model= SignupModel , status_code= status.HTTP_201_CREATED)
async def signup(user: SignupModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this username already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(username=user.username, email=user.email, password=hashed_password, is_staff=user.is_staff, is_active=user.is_active)
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.user_id}
