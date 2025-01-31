from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional

class SignupModel(BaseModel):
    user_id: Optional[int] = None
    username: str
    email: EmailStr
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    @field_validator("user_id")
    def validate_user_id(cls, value):
        if value is not None and value <= 0:
            raise ValueError("user_id must be a positive integer")
        return value

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 3 or len(value) > 25:
            raise ValueError("Username must be between 3 and 25 characters")
        if not value.isalnum():
            raise ValueError("Username must only contain alphanumeric characters")
        return value

    @field_validator("email")
    def validate_email_domain(cls, value):
        valid_domains = ["example.com", "domain.com"]
        domain = value.split("@")[-1]
        if domain not in valid_domains:
            raise ValueError(f"Email domain must be one of {', '.join(valid_domains)}")
        return value

    class Config:
        from_attributes = True
        str_strip_whitespace = True
        str_min_length = 3

class Settings(BaseModel):
    authjwt_secret_key: str = Field(default="8bfcdc4196b345f02b33d21250afb3ff589a98a7dd3a26ddde3874a1b9a894d0")

class LoginModel(BaseModel):
    username: str
    password: str

class OrderModel(BaseModel):
    order_id: Optional[int] = None
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_sizes: Optional[str] = "SMALL"
    user_id: Optional[int] = None

    class Config:
        from_attributes = True