"""
Error handling utilities
"""
from flask import jsonify, request
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ValidationException(Exception):
    """Custom validation exception"""
    def __init__(self, message: str, errors: Dict[str, Any] = None):
        self.message = message
        self.errors = errors or {}
        super().__init__(self.message)

class BusinessRuleException(Exception):
    """Custom business rule exception"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class NotFoundException(Exception):
    """Custom not found exception"""
    def __init__(self, message: str, resource: str = None):
        self.message = message
        self.resource = resource
        super().__init__(self.message)

class UnauthorizedException(Exception):
    """Custom unauthorized exception"""
    def __init__(self, message: str = "Unauthorized access"):
        self.message = message
        super().__init__(self.message)

class ForbiddenException(Exception):
    """Custom forbidden exception"""
    def __init__(self, message: str = "Access forbidden"):
        self.message = message
        super().__init__(self.message)

def handle_validation_error(error: ValidationError):
    """Handle Pydantic validation errors"""
    response = {
        "error": "Validation failed",
        "message": "The request data contains validation errors",
        "details": []
    }
    
    for err in error.errors():
        response["details"].append({
            "field": " -> ".join(str(x) for x in err["loc"]),
            "message": err["msg"],
            "type": err["type"],
            "input": err.get("input")
        })
    
    logger.warning(f"Validation error: {response}")
    return jsonify(response), 400

def handle_validation_exception(error: ValidationException):
    """Handle custom validation exceptions"""
    response = {
        "error": "Validation error",
        "message": error.message,
        "details": error.errors
    }
    
    logger.warning(f"Validation exception: {response}")
    return jsonify(response), 400

def handle_business_rule_exception(error: BusinessRuleException):
    """Handle business rule exceptions"""
    response = {
        "error": "Business rule violation",
        "message": error.message,
        "code": error.code
    }
    
    logger.warning(f"Business rule exception: {response}")
    return jsonify(response), 400

def handle_not_found_exception(error: NotFoundException):
    """Handle not found exceptions"""
    response = {
        "error": "Resource not found",
        "message": error.message,
        "resource": error.resource
    }
    
    logger.info(f"Not found exception: {response}")
    return jsonify(response), 404

def handle_unauthorized_exception(error: UnauthorizedException):
    """Handle unauthorized exceptions"""
    response = {
        "error": "Unauthorized",
        "message": error.message
    }
    
    logger.warning(f"Unauthorized exception: {response}")
    return jsonify(response), 401

def handle_forbidden_exception(error: ForbiddenException):
    """Handle forbidden exceptions"""
    response = {
        "error": "Forbidden",
        "message": error.message
    }
    
    logger.warning(f"Forbidden exception: {response}")
    return jsonify(response), 403

def handle_integrity_error(error: IntegrityError):
    """Handle database integrity errors"""
    error_message = str(error.orig) if hasattr(error, 'orig') else str(error)
    
    # Parse common integrity errors
    if "UNIQUE constraint failed" in error_message:
        if "username" in error_message:
            message = "Username already exists"
        elif "email" in error_message:
            message = "Email already exists"
        else:
            message = "Duplicate entry not allowed"
    elif "FOREIGN KEY constraint failed" in error_message:
        message = "Referenced record does not exist"
    elif "CHECK constraint failed" in error_message:
        message = "Data violates business rules"
    else:
        message = "Database integrity error"
    
    response = {
        "error": "Database error",
        "message": message
    }
    
    logger.error(f"Integrity error: {error_message}")
    return jsonify(response), 400

def handle_http_exception(error: HTTPException):
    """Handle HTTP exceptions"""
    response = {
        "error": error.name,
        "message": error.description,
        "code": error.code
    }
    
    logger.warning(f"HTTP exception: {response}")
    return jsonify(response), error.code

def handle_generic_exception(error: Exception):
    """Handle generic exceptions"""
    response = {
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }
    
    logger.error(f"Generic exception: {str(error)}", exc_info=True)
    return jsonify(response), 500

def register_error_handlers(app):
    """Register all error handlers with Flask app"""
    
    @app.errorhandler(ValidationError)
    def validation_error_handler(error):
        return handle_validation_error(error)
    
    @app.errorhandler(ValidationException)
    def validation_exception_handler(error):
        return handle_validation_exception(error)
    
    @app.errorhandler(BusinessRuleException)
    def business_rule_exception_handler(error):
        return handle_business_rule_exception(error)
    
    @app.errorhandler(NotFoundException)
    def not_found_exception_handler(error):
        return handle_not_found_exception(error)
    
    @app.errorhandler(UnauthorizedException)
    def unauthorized_exception_handler(error):
        return handle_unauthorized_exception(error)
    
    @app.errorhandler(ForbiddenException)
    def forbidden_exception_handler(error):
        return handle_forbidden_exception(error)
    
    @app.errorhandler(IntegrityError)
    def integrity_error_handler(error):
        return handle_integrity_error(error)
    
    @app.errorhandler(HTTPException)
    def http_exception_handler(error):
        return handle_http_exception(error)
    
    @app.errorhandler(Exception)
    def generic_exception_handler(error):
        return handle_generic_exception(error)

def create_success_response(message: str, data: Any = None, status_code: int = 200):
    """Create standardized success response"""
    response = {
        "success": True,
        "message": message
    }
    
    if data is not None:
        response["data"] = data
    
    return jsonify(response), status_code

def create_error_response(message: str, details: Any = None, status_code: int = 400):
    """Create standardized error response"""
    response = {
        "success": False,
        "error": message
    }
    
    if details is not None:
        response["details"] = details
    
    return jsonify(response), status_code

def validate_request_data(schema_class, data: Dict[str, Any]):
    """Validate request data against schema"""
    try:
        validated_data = schema_class(**data)
        return validated_data
    except ValidationError as e:
        raise ValidationException("Request validation failed", format_validation_errors(e))

def format_validation_errors(validation_error: ValidationError) -> Dict[str, Any]:
    """Format validation errors for API response"""
    formatted_errors = {}
    
    for error in validation_error.errors():
        field_path = ".".join(str(x) for x in error["loc"])
        if field_path not in formatted_errors:
            formatted_errors[field_path] = []
        formatted_errors[field_path].append(error["msg"])
    
    return formatted_errors
