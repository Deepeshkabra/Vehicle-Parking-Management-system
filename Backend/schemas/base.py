"""
Base Pydantic models and common validation patterns
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime, time
from typing import Optional, List, Dict, Any
from decimal import Decimal
import re

class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    
    class Config:
        # Allow ORM models to be converted to Pydantic models
        from_attributes = True
        # Validate on assignment
        validate_assignment = True
        # Use enum values instead of names
        use_enum_values = True
        # Custom JSON encoders for special types
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            time: lambda v: v.strftime('%H:%M') if v else None,
            Decimal: lambda v: float(v) if v else None,
        }

class TimestampMixin(BaseModel):
    """Mixin for models with timestamps"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PaginationParams(BaseModel):
    """Common pagination parameters"""
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(10, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(None, description="Sort field")
    sort_order: Optional[str] = Field("asc", pattern ="^(asc|desc)$", description="Sort order")

class PaginatedResponse(BaseModel):
    """Standard paginated response structure"""
    items: List[Any]
    page: int
    per_page: int
    total: int
    pages: int
    has_prev: bool
    has_next: bool
    prev_num: Optional[int] = None
    next_num: Optional[int] = None

class SuccessResponse(BaseModel):
    """Standard success response"""
    message: str
    data: Optional[Any] = None
    
class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    details: Optional[List[Dict[str, Any]]] = None
    field_errors: Optional[Dict[str, List[str]]] = None

# Common validation patterns
def validate_phone_number(phone: str) -> str:
    """Validate phone number format"""
    if not phone:
        return phone
    
    # Remove spaces, hyphens, and parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check for valid international format
    if not re.match(r'^\+?[\d]{10,15}$', cleaned):
        raise ValueError('Invalid phone number format')
    
    return phone

def validate_password_strength(password: str) -> str:
    """Validate password strength"""
    if len(password) < 8:
        raise ValueError('Password must be at least 8 characters long')
    
    if not re.search(r'[A-Z]', password):
        raise ValueError('Password must contain at least one uppercase letter')
    
    if not re.search(r'[a-z]', password):
        raise ValueError('Password must contain at least one lowercase letter')
    
    if not re.search(r'\d', password):
        raise ValueError('Password must contain at least one number')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError('Password must contain at least one special character')
    
    return password

def validate_username(username: str) -> str:
    """Validate username format"""
    if len(username) < 3 or len(username) > 80:
        raise ValueError('Username must be between 3 and 80 characters')
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError('Username can only contain letters, numbers, and underscores')
    
    return username

def validate_pin_code(pin_code: str) -> str:
    """Validate PIN code format"""
    if not pin_code.isdigit():
        raise ValueError('PIN code must contain only digits')
    
    if len(pin_code) < 6 or len(pin_code) > 10:
        raise ValueError('PIN code must be between 6 and 10 digits')
    
    return pin_code

def validate_vehicle_number(vehicle_number: str) -> str:
    """Validate vehicle number format"""
    if not vehicle_number:
        return vehicle_number
    
    # Basic validation - can be extended based on specific requirements
    if len(vehicle_number) > 20:
        raise ValueError('Vehicle number cannot exceed 20 characters')
    
    # Remove spaces and check for basic format
    cleaned = re.sub(r'\s+', '', vehicle_number.upper())
    
    if not re.match(r'^[A-Z0-9]+$', cleaned):
        raise ValueError('Vehicle number can only contain letters and numbers')
    
    return vehicle_number.upper()