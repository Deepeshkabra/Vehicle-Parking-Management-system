# Vehicle Parking Management System - Authentication API

## Overview

This document provides comprehensive information about the authentication system implemented for the Vehicle Parking Management System. The system uses JWT (JSON Web Tokens) for secure authentication and supports two user roles: **Admin** and **User**.

## Features

- **JWT Authentication**: Secure token-based authentication
- **Role-based Access Control**: Admin and User roles
- **Password Security**: Bcrypt hashing with strength validation
- **Token Management**: Access and refresh tokens with blacklisting
- **Input Validation**: Pydantic schemas for data validation
- **Error Handling**: Comprehensive error responses

## API Endpoints

### Base URL
```
http://localhost:5000
```

### 1. Admin Login
**Endpoint**: `POST /api/auth/admin/login`

**Description**: Authenticates admin users using configured credentials.

**Request Body**:
```json
{
    "username": "admin@example.com",
    "password": "admin123"
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "Admin login successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "role": "admin",
            "is_active": true,
            "created_at": "2024-01-01T00:00:00",
            "last_login": "2024-01-15T10:30:00"
        }
    }
}
```

**Error Response** (401):
```json
{
    "success": false,
    "error": "Invalid admin credentials"
}
```

### 2. User Registration
**Endpoint**: `POST /api/auth/register`

**Description**: Registers new users with automatic role assignment.

**Request Body**:
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "phone": "+1234567890"
}
```

**Password Requirements**:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

**Success Response** (201):
```json
{
    "success": true,
    "message": "Registration successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 2,
            "username": "john_doe",
            "email": "john@example.com",
            "role": "user",
            "phone": "+1234567890",
            "is_active": true,
            "created_at": "2024-01-15T10:30:00"
        }
    }
}
```

**Error Response** (400):
```json
{
    "success": false,
    "error": "Request validation failed",
    "details": {
        "email": ["This email is already registered"],
        "password": ["Password must contain at least one uppercase letter"]
    }
}
```

### 3. User Login
**Endpoint**: `POST /api/auth/login`

**Description**: Authenticates registered users using username or email.

**Request Body**:
```json
{
    "username": "john_doe",
    "password": "SecurePass123!",
    "remember_me": false
}
```

**Note**: The `username` field accepts both username and email address.

**Success Response** (200):
```json
{
    "success": true,
    "message": "Login successful",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 2,
            "username": "john_doe",
            "email": "john@example.com",
            "role": "user",
            "phone": "+1234567890",
            "is_active": true,
            "last_login": "2024-01-15T10:30:00"
        }
    }
}
```

### 4. Token Refresh
**Endpoint**: `POST /api/auth/refresh`

**Description**: Generates a new access token using a valid refresh token.

**Headers**:
```
Authorization: Bearer <refresh_token>
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "Token refreshed successfully",
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "user": {
            "id": 2,
            "username": "john_doe",
            "email": "john@example.com",
            "role": "user"
        }
    }
}
```

### 5. Logout
**Endpoint**: `POST /api/auth/logout`

**Description**: Invalidates the current access token by adding it to the blacklist.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "Logout successful"
}
```

### 6. Get Current User
**Endpoint**: `GET /api/auth/me`

**Description**: Retrieves current user information from the access token.

**Headers**:
```
Authorization: Bearer <access_token>
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "User information retrieved",
    "data": {
        "user": {
            "id": 2,
            "username": "john_doe",
            "email": "john@example.com",
            "role": "user",
            "phone": "+1234567890",
            "is_active": true,
            "created_at": "2024-01-15T10:30:00",
            "last_login": "2024-01-15T10:30:00"
        }
    }
}
```

## JWT Token Structure

### Access Token Claims
```json
{
    "sub": 2,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true,
    "iat": 1642248600,
    "exp": 1642252200,
    "jti": "unique-token-id"
}
```

### Token Expiry
- **Access Token**: 1 hour (configurable)
- **Refresh Token**: 30 days (configurable)
- **Remember Me**: 7 days for access token

## Configuration

### Environment Variables
```bash
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour in seconds
JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 days in seconds

# Admin Credentials
ADMIN_EMAIL=admin@yourcompany.com
ADMIN_PASSWORD=SecureAdminPass123!
ADMIN_NAME=System Administrator

# Database
DATABASE_URL=sqlite:///parking_app.db

# Flask
SECRET_KEY=your-flask-secret-key
DEBUG=True
```

### Configuration Class Updates
The following JWT settings are automatically configured:

```python
class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
```

## Usage Examples

### Using cURL

#### Admin Login
```bash
curl -X POST http://localhost:5000/api/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin@example.com",
    "password": "admin123"
  }'
```

#### User Registration
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "phone": "+1234567890"
  }'
```

#### User Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john@example.com",
    "password": "SecurePass123!"
  }'
```

#### Protected Endpoint Access
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

### Using JavaScript/Frontend

#### Login Function
```javascript
async function loginUser(username, password) {
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
                remember_me: false
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Store tokens
            localStorage.setItem('access_token', data.data.access_token);
            localStorage.setItem('refresh_token', data.data.refresh_token);
            localStorage.setItem('user', JSON.stringify(data.data.user));
            
            return { success: true, user: data.data.user };
        } else {
            return { success: false, error: data.error };
        }
    } catch (error) {
        return { success: false, error: 'Network error' };
    }
}
```

#### Authenticated Request Function
```javascript
async function makeAuthenticatedRequest(url, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const config = {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
            ...options.headers,
        },
    };
    
    try {
        const response = await fetch(url, config);
        
        if (response.status === 401) {
            // Token expired, try to refresh
            const refreshed = await refreshToken();
            if (refreshed) {
                // Retry original request with new token
                config.headers.Authorization = `Bearer ${localStorage.getItem('access_token')}`;
                return await fetch(url, config);
            } else {
                // Refresh failed, redirect to login
                window.location.href = '/login';
                return null;
            }
        }
        
        return response;
    } catch (error) {
        console.error('Request failed:', error);
        throw error;
    }
}
```

## Security Considerations

### Password Security
- Passwords are hashed using Werkzeug's `generate_password_hash` with bcrypt
- Password strength validation enforces complex passwords
- No plain text passwords are stored in the database

### JWT Security
- Tokens are signed with a configurable secret key
- Access tokens have short expiry times (1 hour default)
- Refresh tokens have longer expiry times (30 days default)
- Token blacklisting prevents use of revoked tokens
- JTI (JWT ID) is used for tracking individual tokens

### Input Validation
- All input is validated using Pydantic schemas
- Email format validation ensures proper email addresses
- Username validation prevents special characters
- Phone number validation ensures proper format

### Error Handling
- Generic error messages prevent information disclosure
- Detailed validation errors help with debugging
- All errors are logged for monitoring
- Consistent error response format

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT 1,
    phone VARCHAR(15),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    CONSTRAINT valid_role CHECK (role IN ('user', 'admin'))
);
```

## Installation and Setup

### 1. Install Dependencies
```bash
cd Backend
pip install -r requirements.txt
# or using uv
uv pip install flask flask-sqlalchemy flask-jwt-extended pydantic email-validator
```

### 2. Set Environment Variables
```bash
export JWT_SECRET_KEY="your-super-secret-jwt-key"
export ADMIN_EMAIL="admin@yourcompany.com"
export ADMIN_PASSWORD="SecureAdminPass123!"
export SECRET_KEY="your-flask-secret-key"
```

### 3. Initialize Database
```bash
python app.py
```

The database and admin user will be created automatically on first run.

### 4. Test the API
```bash
# Check if API is running
curl http://localhost:5000/api/health

# Test admin login
curl -X POST http://localhost:5000/api/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin@example.com", "password": "admin123"}'
```

## Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | Validation Error | Invalid input data or format |
| 401 | Unauthorized | Invalid credentials or expired token |
| 403 | Forbidden | Insufficient permissions or inactive account |
| 409 | Conflict | Username or email already exists |
| 422 | Unprocessable Entity | Invalid token format |
| 500 | Internal Server Error | Unexpected server error |

## Testing

### Unit Tests
The authentication system includes comprehensive error handling and validation. Consider adding unit tests for:

- User registration validation
- Password strength verification
- JWT token generation and validation
- Role-based access control
- Token blacklisting functionality

### Integration Tests
Test the complete authentication flow:

- User registration → Login → Protected endpoint access
- Admin login → Protected admin endpoint access
- Token refresh → Continued access
- Logout → Token invalidation

## Future Enhancements

- **Redis Integration**: Move token blacklisting to Redis for scalability
- **Email Verification**: Add email verification for new user registrations
- **Password Reset**: Implement secure password reset functionality
- **Rate Limiting**: Add rate limiting for authentication attempts
- **Audit Logging**: Track all authentication events
- **Multi-factor Authentication**: Add 2FA support
- **Session Management**: Advanced session handling and monitoring

## Support

For issues or questions regarding the authentication system:

1. Check the error response for detailed validation messages
2. Verify environment variables are set correctly
3. Ensure database tables are created properly
4. Check server logs for detailed error information

The authentication system is designed to be secure, scalable, and maintainable while providing a smooth user experience for both admin and user roles in the Vehicle Parking Management System. 