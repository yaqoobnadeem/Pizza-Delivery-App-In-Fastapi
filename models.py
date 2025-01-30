from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True) 
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship("Choice", back_populates="user")  
      
    def __repr__(self):
        return f"<User {self.username}>"

class Choice(Base):
    ORDER_STATUS = (("PENDING", "pending"), ("IN-TRANSIT", "in-transit"), ("DELIVERED", "delivered"))
    PIZZA_SIZES = (("SMALL", "small"), ("MEDIUM", "medium"), ("LARGE", "large"), ("EXTRA-LARGE", "extra-large"))
    
    __tablename__ = "pizza_order"  
    order_id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default="PENDING")
    pizza_sizes = Column(ChoiceType(choices=PIZZA_SIZES), default="SMALL")
    user_id = Column(Integer, ForeignKey("user.user_id"))
    user = relationship("User", back_populates="orders")  
    
    def __repr__(self):
        return f"<Order {self.order_id}>"
