"""
User validation schemas
"""
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List
from datetime import datetime
from .base import BaseSchema, TimestampMixin, validate_username, validate_phone_number, validate_password_strength

class UserBase(BaseSchema):
    """Base user schema with common fields"""
    username: str = Field(..., min_length=3, max_length=80, description="Username")
    email: EmailStr = Field(..., description="Email address")
    phone: Optional[str] = Field(None, max_length=15, description="Phone number")
    
    @field_validator('username')
    def validate_username_format(cls, v):
        return validate_username(v)
    
    @field_validator('phone')
    def validate_phone_format(cls, v):
        if v:
            return validate_phone_number(v)
        return v

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., description="Password confirmation")
    
    @field_validator('password')
    def validate_password_strength(cls, v):
        return validate_password_strength(v)
    
    @field_validator('confirm_password')
    def validate_passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "SecurePass123!",
                "confirm_password": "SecurePass123!",
                "phone": "+1234567890"
            }
        }

class UserLogin(BaseSchema):
    """Schema for user login"""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")
    remember_me: Optional[bool] = Field(False, description="Remember login")
    
    class Config:
        schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "SecurePass123!",
                "remember_me": False
            }
        }

class UserUpdate(BaseSchema):
    """Schema for user profile updates"""
    email: Optional[EmailStr] = Field(None, description="New email address")
    phone: Optional[str] = Field(None, max_length=15, description="New phone number")
    current_password: Optional[str] = Field(None, description="Current password (required for email change)")
    new_password: Optional[str] = Field(None, min_length=8, description="New password")
    confirm_password: Optional[str] = Field(None, description="Confirm new password")
    
    @field_validator('phone')
    def validate_phone_format(cls, v):
        if v:
            return validate_phone_number(v)
        return v
    
    @field_validator('new_password')
    def validate_new_password_strength(cls, v):
        if v:
            return validate_password_strength(v)
        return v
    
    @field_validator('confirm_password')
    def validate_passwords_match(cls, v, values):
        if v and 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
    
    @field_validator('current_password')
    def validate_current_password_required(cls, v, values):
        if ('email' in values and values['email']) or ('new_password' in values and values['new_password']):
            if not v:
                raise ValueError('Current password is required for email or password changes')
        return v

class UserResponse(UserBase, TimestampMixin):
    """Schema for user API responses"""
    id: int
    role: str = Field(..., description="User role")
    is_active: bool = Field(..., description="Account status")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "username": "john_doe",
                "email": "john@example.com",
                "role": "user",
                "phone": "+1234567890",
                "is_active": True,
                "last_login": "2024-01-15T10:30:00",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-15T10:30:00"
            }
        }

class UserList(BaseSchema):
    """Schema for user list responses"""
    users: List[UserResponse]
    total: int
    page: int
    per_page: int
    
class UserPasswordReset(BaseSchema):
    """Schema for password reset request"""
    email: EmailStr = Field(..., description="Email address")
    
class UserPasswordResetConfirm(BaseSchema):
    """Schema for password reset confirmation"""
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=8, description="New password")
    confirm_password: str = Field(..., description="Confirm new password")
    
    @field_validator('new_password')
    def validate_password_strength(cls, v):
        return validate_password_strength(v)
    
    @field_validator('confirm_password')
    def validate_passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v
