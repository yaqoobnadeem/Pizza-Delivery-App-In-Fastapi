from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from models import User, Choice
from schemas import OrderModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

Order_router = APIRouter()
session = Session(bind=engine)

@Order_router.get("/")
async def n(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    return {"message": "Authorized"}

@Order_router.post("/order")
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()
    
    user = session.query(User).filter(User.username == current_user).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    new_order = Choice(
        pizza_size=order.pizza_size, 
        quantity=order.quantity
    )
    
    new_order.user = user
    
    session.add(new_order)
    session.commit()
    session.refresh(new_order)  

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)
