from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re


class SignupModel(BaseModel):
    user_id: Optional[int]
    username: str
    email: EmailStr
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 25:
            raise ValueError('Username must be between 3 and 25 characters')
        if not v.isalnum():
            raise ValueError('Username must only contain alphanumeric characters')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in v):
            raise ValueError('Password must contain at least one special character')
        return v

    @validator('email')
    def validate_email_domain(cls, v):
        valid_domains = ['example.com', 'domain.com']
        domain = v.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f'Email domain must be one of {", ".join(valid_domains)}')
        return v

    @validator('is_staff', 'is_active', pre=True, always=True)
    def validate_boolean(cls, v):
        return v if v is not None else False

    class Config:
        orm_mode = True