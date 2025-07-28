"""
Authentication routes for Vehicle Parking Management System
Handles user registration, login, admin authentication, and JWT token management
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

# Import admin credentials from config
from config import Config

# Import models and utilities
from models import db, User
from schemas.user import UserLogin, UserCreate, UserResponse
from utils.error_handlers import (
    ValidationException,
    UnauthorizedException,
    ForbiddenException,
    create_success_response,
    create_error_response,
    validate_request_data,
)
from utils.validation_utils import validate_user_permissions

# Create blueprint for authentication routes
auth_bp = Blueprint("auth", __name__)

# JWT token blacklist (in production, use Redis or database)
blacklisted_tokens = set()


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    Unified login endpoint for both admin and users

    Expected JSON body:
    {
        "username": "user@example.com or username or admin@example.com",
        "password": "password123",
        "remember_me": false
    }

    Returns:
    {
        "success": true,
        "message": "Login successful",
        "data": {
            "access_token": "eyJ...",
            "refresh_token": "eyJ...",
            "user": {...}
        }
    }
    """
    try:
        # Get request data
        data = request.get_json()
        if not data:
            raise ValidationException("Request body is required")

        # First check if this is admin login attempt
        admin_email = Config.ADMIN_EMAIL
        print(admin_email)
        admin_password = Config.ADMIN_PASSWORD
        print(admin_password)
        if (
            data.get("email") == admin_email.lower()
            and data.get("password") == admin_password
        ):

            # Generate JWT tokens for admin
            tokens = generate_admin_tokens(admin_email)

            # Prepare admin response data
            admin_data = {
                "id": "admin0",
                "username": "admin",
                "email": admin_email,
                "role": "admin",
                "is_active": True,
                "created_at": None,
                "last_login": datetime.now().isoformat(),
                "phone": None,
            }

            return create_success_response(
                "Admin login successful",
                {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "user": admin_data,
                },
            )

        # If not admin, proceed with regular user login
        # Validate request data using UserLogin schema
        login_data = validate_request_data(UserLogin, data)
        # Find user by username or email
        user = find_user_by_username_or_email(login_data.username)
        if not user:
            raise UnauthorizedException("Invalid username/email or password")

        # Verify password
        if not user.check_password(login_data.password):
            raise UnauthorizedException("Invalid username/email or password")

        # Check if user account is active
        if not user.is_active:
            raise ForbiddenException(
                "Account is inactive. Please contact administrator."
            )

        # Update last login timestamp
        user.last_login = datetime.now()
        db.session.commit()

        # Generate JWT tokens
        tokens = generate_user_tokens(user)

        # Adjust token expiry for "remember me" functionality
        if login_data.remember_me:
            # Extend access token expiry for remember me
            tokens["access_token"] = create_access_token(
                identity=user.id,
                additional_claims={
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "is_active": user.is_active,
                },
                expires_delta=timedelta(days=7),  # 7 days for remember me
            )

        # Prepare user response data
        user_data = UserResponse.model_validate(user).model_dump()

        return create_success_response(
            "Login successful",
            {
                "access_token": tokens["access_token"],
                "refresh_token": tokens["refresh_token"],
                "user": user_data,
            },
        )

    except ValidationException as e:
        return create_error_response(e.message, e.errors, 400)
    except UnauthorizedException as e:
        return create_error_response(e.message, status_code=401)
    except ForbiddenException as e:
        return create_error_response(e.message, status_code=403)
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    """
    User registration endpoint
    """
    try:
        # Get request data
        data = request.get_json()
        print(data["username"])

        if not data:
            raise ValidationException("Request body is required")

        new_user = validate_and_create_user(data)
        print(new_user)

        return create_success_response("User registered successfully", new_user)

    except ValidationException as e:
        return create_error_response(e.message, e.errors, 400)
    except Exception as e:
        current_app.logger.error(f"Registration error: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


@auth_bp.route("/api/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    """
    Token refresh endpoint
    Requires a valid refresh token in Authorization header
    Handles both admin and user token refresh

    Returns:
    {
        "success": true,
        "message": "Token refreshed successfully",
        "data": {
            "access_token": "eyJ...",
            "user": {...}
        }
    }
    """
    try:
        # Get current user ID from refresh token
        current_user_id = get_jwt_identity()
        print(f"Refresh token request - User ID: {current_user_id}")

        # Get the full JWT payload for debugging
        jwt_payload = get_jwt()
        print(f"JWT payload: {jwt_payload}")
        print(f"Token type: {jwt_payload.get('type', 'unknown')}")

        # Check if this is an admin token
        if current_user_id == "admin":
            # Handle admin token refresh
            admin_email = Config.ADMIN_EMAIL
            if not admin_email:
                raise UnauthorizedException("Admin configuration not found")

            # Generate new access token for admin
            additional_claims = {
                "username": "admin",
                "email": admin_email,
                "role": "admin",
                "is_active": True,
            }

            new_access_token = create_access_token(
                identity="admin",
                additional_claims=additional_claims,
                expires_delta=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
            )

            # Prepare admin response data
            admin_data = {
                "id": "admin",
                "username": "admin",
                "email": admin_email,
                "role": "admin",
                "is_active": True,
                "created_at": None,
                "last_login": datetime.now().isoformat(),
                "phone": None,
            }

            return create_success_response(
                "Admin token refreshed successfully",
                {"access_token": new_access_token, "user": admin_data},
            )

        # Handle regular user token refresh
        # Get user from database
        user = User.query.get(current_user_id)
        if not user:
            raise UnauthorizedException("User not found")

        # Check if user account is still active
        if not user.is_active:
            raise ForbiddenException("Account is inactive")

        # Generate new access token
        additional_claims = {
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }

        new_access_token = create_access_token(
            identity=user.id,
            additional_claims=additional_claims,
            expires_delta=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
        )

        # Prepare user response data
        user_data = UserResponse.from_orm(user).dict()

        return create_success_response(
            "Token refreshed successfully",
            {"access_token": new_access_token, "user": user_data},
        )

    except UnauthorizedException as e:
        return create_error_response(e.message, status_code=401)
    except ForbiddenException as e:
        return create_error_response(e.message, status_code=403)
    except Exception as e:
        current_app.logger.error(f"Token refresh error: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


@auth_bp.route("/api/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout endpoint
    Requires a valid access token in Authorization header
    Adds token to blacklist to prevent further use

    Returns:
    {
        "success": true,
        "message": "Logout successful"
    }
    """
    try:
        # Get current token JTI (JWT ID) for blacklisting
        token = get_jwt()
        jti = token["jti"]

        # Add token to blacklist
        blacklisted_tokens.add(jti)

        return create_success_response("Logout successful")

    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


@auth_bp.route("/api/auth/me", methods=["GET"])
@jwt_required()
def get_current_user():
    """
    Get current user information
    Requires a valid access token in Authorization header
    Handles both admin and user information retrieval

    Returns:
    {
        "success": true,
        "message": "User information retrieved",
        "data": {
            "user": {...}
        }
    }
    """
    try:
        # Get current user ID from token
        current_user_id = get_jwt_identity()

        # Check if this is an admin token
        if current_user_id == "admin":
            admin_email = current_app.config.get("ADMIN_EMAIL")
            if not admin_email:
                raise UnauthorizedException("Admin configuration not found")

            # Prepare admin response data
            admin_data = {
                "id": "admin",
                "username": "admin",
                "email": admin_email,
                "role": "admin",
                "is_active": True,
                "created_at": None,
                "last_login": datetime.now().isoformat(),
                "phone": None,
            }

            return create_success_response(
                "Admin information retrieved", {"user": admin_data}
            )

        # Handle regular user information retrieval
        # Get user from database
        user = User.query.get(current_user_id)
        if not user:
            raise UnauthorizedException("User not found")

        # Check if user account is still active
        if not user.is_active:
            raise ForbiddenException("Account is inactive")

        # Prepare user response data
        user_data = UserResponse.from_orm(user).dict()

        return create_success_response(
            "User information retrieved", {"user": user_data}
        )

    except UnauthorizedException as e:
        return create_error_response(e.message, status_code=401)
    except ForbiddenException as e:
        return create_error_response(e.message, status_code=403)
    except Exception as e:
        current_app.logger.error(f"Get current user error: {str(e)}")
        return create_error_response("Internal server error", status_code=500)


def generate_user_tokens(user):
    """
    Generate access and refresh tokens for user

    Args:
        user: User model instance

    Returns:
        dict: Dictionary containing access_token and refresh_token
    """
    # Create additional claims for JWT payload
    additional_claims = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
    }

    # Generate access token (short-lived)
    access_token = create_access_token(
        identity=user.id,
        additional_claims=additional_claims,
        expires_delta=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
    )

    # Generate refresh token (long-lived)
    refresh_token = create_refresh_token(
        identity=user.id, expires_delta=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def generate_admin_tokens(admin_email):
    """
    Generate access and refresh tokens for admin user

    Args:
        admin_email: Admin email from config

    Returns:
        dict: Dictionary containing access_token and refresh_token
    """
    # Create additional claims for JWT payload for admin
    additional_claims = {
        "username": "admin",
        "email": admin_email,
        "role": "admin",
        "is_active": True,
    }

    # Generate access token (short-lived) - using 'admin' as identity
    access_token = create_access_token(
        identity="admin",
        additional_claims=additional_claims,
        expires_delta=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"],
    )

    # Generate refresh token (long-lived)
    refresh_token = create_refresh_token(
        identity="admin", expires_delta=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def find_user_by_username_or_email(identifier):
    """
    Find user by username or email

    Args:
        identifier: Username or email string

    Returns:
        User: User model instance or None
    """
    # Try to find user by email first
    user = User.query.filter_by(email=identifier.lower()).first()

    # If not found by email, try username
    if not user:
        user = User.query.filter_by(username=identifier).first()

    return user


def validate_and_create_user(user_data):
    """
    Validate user data and create new user

    Args:
        user_data: Dictionary containing user information

    Returns:
        User: Created user instance

    Raises:
        ValidationException: If validation fails
        IntegrityError: If username/email already exists
    """
    # Check if username already exists
    existing_user = User.query.filter_by(username=user_data["username"]).first()
    if existing_user:
        raise ValidationException(
            "Username already exists", {"username": ["This username is already taken"]}
        )

    # Check if email already exists
    existing_email = User.query.filter_by(email=user_data["email"].lower()).first()
    if existing_email:
        raise ValidationException(
            "Email already exists", {"email": ["This email is already registered"]}
        )

    # Create new user
    new_user = User(
        username=user_data["username"],
        email=user_data["email"].lower(),
        role="user",  # Default role for new users
        phone=user_data["phone"],
        is_active=True,
    )

    # Set password using model method
    new_user.set_password(user_data["password"])
    db.session.add(new_user)
    db.session.commit()

    return new_user.to_dict()


# JWT error handlers
@auth_bp.errorhandler(422)
def handle_unprocessable_entity(e):
    """Handle JWT decode errors"""
    return create_error_response("Invalid token format", status_code=422)


@auth_bp.errorhandler(401)
def handle_unauthorized(e):
    """Handle JWT unauthorized errors"""
    return create_error_response("Token is invalid or expired", status_code=401)


# JWT token blacklist checker
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Check if JWT token is blacklisted
    This function is called by Flask-JWT-Extended for every protected endpoint
    """
    jti = jwt_payload["jti"]
    return jti in blacklisted_tokens
