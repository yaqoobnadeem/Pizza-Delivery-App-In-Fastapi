from pydantic import BaseModel, EmailStr
from typing import Optional

class SignupModel(BaseModel):
    user_id: Optional[int]
    username: str
    email: EmailStr
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    def __init__(self, **data):
        super().__init__(**data)

        if self.user_id is not None and self.user_id <= 0:
            raise ValueError('user_id must be a positive integer')

        
        if len(self.username) < 3 or len(self.username) > 25:
            raise ValueError('Username must be between 3 and 25 characters')
        if not self.username.isalnum():
            raise ValueError('Username must only contain alphanumeric characters')

        valid_domains = ['example.com', 'domain.com']
        domain = self.email.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f'Email domain must be one of {", ".join(valid_domains)}')

    class Config:
        from_attributes = True  

class Settings(BaseModel):
    authjwt_secret_key: str = '8bfcdc4196b345f02b33d21250afb3ff589a98a7dd3a26ddde3874a1b9a894d0'

class LoginModel(BaseModel):
    username: str
    password: str

class OrderModel(BaseModel):
    order_id : Optional[int]
    quantity : int
    order_status : Optional[str] = "PENDING" 
    pizza_sizes : Optional[str] = "SMALL"
    user_id : Optional[int]
    
    class Config:
        orm_model  = True
      
    