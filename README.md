# Vehicle Parking Management System - Project Report

## Author
**[Deepesh Kabra]**  
**[22F3001136]**  
**[22f3001136@ds.study.iitm.ac.in]**  

I am a Computer Science student passionate about full-stack web development and database design. This project demonstrates my skills in building scalable web applications using modern technologies like Flask, Vue.js, and implementing complex features like authentication, background jobs, and real-time data management.

## Description
This project is a comprehensive multi-user Vehicle Parking Management System designed to handle parking lot operations efficiently. The system supports two user roles - Admin (superuser) for managing parking lots and viewing analytics, and Users for booking parking spots and tracking their parking history. The application implements role-based access control, automatic spot allocation, real-time availability tracking, and background job processing for reports and notifications.

**AI/LLM Usage: 15-20%** - Used AI assistance primarily for code optimization, error handling patterns, and documentation formatting. All core logic, database design, API architecture, and business rules were implemented independently with original problem-solving approaches.

## Technologies Used

### Backend Technologies
- **Flask 3.1.1** - Main web framework for building RESTful APIs
- **Flask-SQLAlchemy 3.1.1** - ORM for database operations and model definitions
- **Flask-JWT-Extended 4.6.0** - JWT authentication and authorization management
- **PyJWT 2.9.0** - JSON Web Token implementation for secure authentication
- **Pydantic 2.11.7** - Data validation and serialization for API request/response schemas
- **Flask-CORS 6.0.1** - Cross-Origin Resource Sharing for frontend-backend communication
- **Flask-Mail 0.10.0** - Email functionality for notifications and reports

### Background Processing & Caching
- **Celery 5.5.3** - Asynchronous task processing for CSV exports and scheduled jobs
- **Redis 6.2.0** - Message broker for Celery and caching layer for performance optimization
- **Crontab 1.0.5** - Scheduled task management for daily reminders and monthly reports

### Data Visualization & Reporting
- **Matplotlib 3.10.3** - Chart generation for dashboard analytics and reports
- **Seaborn 0.13.2** - Statistical data visualization for parking usage patterns

### Frontend Technologies
- **Vue.js 3** - Progressive JavaScript framework for building reactive user interfaces
- **Bootstrap 5** - CSS framework for responsive design and component styling
- **Vite** - Build tool for fast development and optimized production builds

### Database & Development
- **SQLite** - Lightweight database for development and demonstration
- **Black 25.1.0** - Code formatter for maintaining Python code quality

### Purpose Behind Technology Choices
- **Flask** chosen for its simplicity and flexibility in building RESTful APIs
- **Vue.js** selected for reactive frontend with component-based architecture
- **JWT** implemented for stateless authentication suitable for SPA applications
- **Redis** used for both caching frequent database queries and Celery message brokering
- **Celery** enables background processing for time-intensive operations like CSV generation
- **Pydantic** ensures robust data validation and automatic API documentation
- **SQLAlchemy** provides powerful ORM capabilities with relationship management

## DB Schema Design

### Core Tables Structure

#### 1. Users Table
```sql
users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    phone VARCHAR(15),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    
    CONSTRAINT valid_role CHECK (role IN ('user', 'admin')),
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_created_at (created_at)
)
```

#### 2. Parking Lots Table
```sql
parking_lots (
    id INTEGER PRIMARY KEY,
    prime_location_name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    pin_code VARCHAR(10) NOT NULL,
    number_of_spots INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    description TEXT,
    operating_hours_start TIME,
    operating_hours_end TIME,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT positive_spots CHECK (number_of_spots > 0),
    CONSTRAINT non_negative_price CHECK (price >= 0),
    INDEX idx_location (prime_location_name),
    INDEX idx_pin_code (pin_code),
    INDEX idx_created_at (created_at)
)
```

#### 3. Parking Spots Table
```sql
parking_spots (
    id INTEGER PRIMARY KEY,
    lot_id INTEGER NOT NULL,
    spot_number INTEGER NOT NULL,
    status VARCHAR(1) NOT NULL DEFAULT 'A',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (lot_id) REFERENCES parking_lots(id) ON DELETE CASCADE,
    CONSTRAINT valid_status CHECK (status IN ('A', 'O')),
    CONSTRAINT positive_spot_number CHECK (spot_number > 0),
    CONSTRAINT unique_spot_per_lot UNIQUE (lot_id, spot_number),
    INDEX idx_lot_id (lot_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
)
```

#### 4. Reservations Table
```sql
reservations (
    id INTEGER PRIMARY KEY,
    spot_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    parking_timestamp DATETIME NOT NULL,
    leaving_timestamp DATETIME,
    expected_leaving_time DATETIME,
    parking_cost DECIMAL(10,2) DEFAULT 0.0,
    hourly_rate DECIMAL(10,2) NOT NULL,
    vehicle_number VARCHAR(20),
    vehicle_model VARCHAR(50),
    vehicle_color VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    remarks TEXT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (spot_id) REFERENCES parking_spots(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT valid_reservation_status CHECK (status IN ('active', 'completed', 'cancelled')),
    CONSTRAINT non_negative_cost CHECK (parking_cost >= 0),
    CONSTRAINT positive_hourly_rate CHECK (hourly_rate > 0),
    INDEX idx_spot_id (spot_id),
    INDEX idx_user_id (user_id),
    INDEX idx_parking_timestamp (parking_timestamp),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
)
```

### Schema Design Rationale
- **Normalization**: Database follows 3NF with proper foreign key relationships to eliminate redundancy
- **Indexing Strategy**: Strategic indexes on frequently queried columns (user_id, lot_id, status, timestamps)
- **Constraints**: Business logic enforced at database level with check constraints for data integrity
- **Cascading Deletes**: Proper cascade rules ensure referential integrity when parking lots are deleted
- **Flexible Status Management**: Enum-style status fields allow for future expansion of booking states
- **Timestamp Tracking**: Comprehensive audit trail with created_at/updated_at on all entities
- **Scalability Considerations**: Design supports multiple parking lots and concurrent user operations

## API Design

The API follows RESTful design principles with clear resource-based endpoints organized into logical modules:

### Authentication Module (`/api/auth/`)
- **JWT-based authentication** with access and refresh token pattern
- **Unified login endpoint** supporting both admin and user authentication
- **Secure password handling** with bcrypt hashing
- **Token blacklisting** for secure logout functionality

### Admin Module (`/api/admin/`)
- **User management** endpoints for viewing all registered users
- **Parking lot CRUD operations** with validation and business logic
- **Role-based authorization** ensuring only admin access
- **Comprehensive error handling** with detailed logging

### User Module (`/api/user/`)
- **Profile management** for user account operations
- **Parking lot browsing** with availability information
- **Booking system** with automatic spot allocation
- **Reservation management** including release and history tracking
- **CSV export functionality** with async background processing

### Key API Implementation Features
- **Consistent response format** with success/error structure across all endpoints
- **Request validation** using Pydantic schemas for type safety
- **Caching layer** with Redis for performance optimization
- **Background job integration** for time-intensive operations
- **Comprehensive error handling** with appropriate HTTP status codes
- **API documentation** available in separate YAML file following OpenAPI 3.0 specification

## Architecture and Features

### Project Organization
The project follows a modular architecture with clear separation of concerns:

**Backend Structure (`/Backend/`):**
- `models/` - SQLAlchemy database models with business logic methods
- `routes/` - Flask blueprints organizing API endpoints by functionality (auth, admin, user)
- `schemas/` - Pydantic models for request/response validation and serialization
- `utils/` - Utility modules for caching, error handling, validation, and notifications
- `jobs/` - Celery task definitions for background processing and scheduled jobs
- `config.py` - Centralized configuration management with environment variable support
- `app.py` - Flask application factory with extension initialization

**Frontend Structure (`/frontend/`):**
- `src/components/` - Vue.js components organized by user role (admin/, user/, auth/)
- `src/views/` - Page-level Vue components for different application sections
- `src/services/` - API service layer for backend communication
- `src/stores/` - Pinia state management for authentication and application state
- `src/router/` - Vue Router configuration for SPA navigation

### Implemented Features

#### Core Features (Required)
- **Multi-role Authentication System**: JWT-based authentication supporting admin and user roles with secure token management
- **Parking Lot Management**: Complete CRUD operations for parking lots with automatic spot generation
- **Automatic Spot Allocation**: First-available spot assignment without user selection
- **Real-time Availability Tracking**: Live status updates for parking spots with occupancy monitoring
- **Reservation System**: Full booking lifecycle from creation to completion with cost calculation
- **User Dashboard**: Comprehensive interface showing booking history and current reservations
- **Admin Dashboard**: Administrative interface for lot management and user oversight

#### Advanced Features (Additional)
- **Background Job Processing**: Celery-powered async tasks for CSV exports and email notifications
- **Caching System**: Redis-based caching for improved performance on frequent queries
- **CSV Export Functionality**: Asynchronous generation and email delivery of parking history reports
- **Comprehensive Validation**: Multi-layer validation using Pydantic schemas and database constraints
- **Error Handling & Logging**: Structured error responses with detailed server-side logging
- **Responsive Design**: Bootstrap-powered responsive UI supporting mobile and desktop
- **API Documentation**: Complete OpenAPI specification with request/response examples

#### Technical Implementation Highlights
- **Database Relationships**: Proper foreign key relationships with cascade operations
- **Security Implementation**: Password hashing, JWT token validation, and role-based access control
- **Performance Optimization**: Database indexing, query optimization, and Redis caching
- **Scalable Architecture**: Modular design supporting future feature additions
- **Development Best Practices**: Code formatting, error handling, and comprehensive logging
- **Business Logic Enforcement**: Database constraints and application-level validation ensuring data integrity

The system successfully demonstrates enterprise-level web application development with modern technologies, proper security practices, and scalable architecture suitable for real-world parking management scenarios.
```
