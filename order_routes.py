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


@Order_router.get("/orders")
async def list_all_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    current_user = Authorize.get_jwt_subject()
    
    user = session.query(User).filter(User.username == current_user).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not a superuser")
    
    orders = session.query(Choice).all()
    return jsonable_encoder(orders)

 
@Order_router.get("/orders/{id}")
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    user = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.username == user).first()

    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not current_user.is_staff:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not allowed to carry out request")

    order = session.query(Choice).filter(Choice.id == id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    return jsonable_encoder(order)

 
@Order_router.get("/user/orders")
async def get_user_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    user = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.username == user).first()

    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return jsonable_encoder(current_user.orders)


@Order_router.get("/user/order/{order_id}/")
async def get_specific_order(order_id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    subject = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.username == subject).first()

    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    orders = current_user.orders
    
    for o in orders:
        if o.id == order_id:
            return jsonable_encoder(o)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No order with such ID")