"""
Secure Flask API - Fixed Version
This code addresses all security vulnerabilities identified in the code review.
"""

import logging
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta

import bcrypt
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import BadRequest

# Load environment variables
load_dotenv()

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Initialize Flask app with security configurations
app = Flask(__name__)

# Security Configuration
app.config["SECRET_KEY"] = os.environ.get("API_SECRET")
if not app.config["SECRET_KEY"]:
    raise ValueError("API_SECRET environment variable is required")

# Rate limiting configuration
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=os.environ.get("RATELIMIT_STORAGE_URL", "memory://"),
)
limiter.init_app(app)

# Database configuration
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///users.db")


class SecurityError(Exception):
    """Custom exception for security-related errors"""

    pass


class DatabaseError(Exception):
    """Custom exception for database-related errors"""

    pass


@contextmanager
def get_db_connection():
    """Secure database connection with proper error handling"""
    conn = None
    try:
        if DATABASE_URL.startswith("sqlite"):
            # Extract database path from URL
            db_path = DATABASE_URL.replace("sqlite:///", "")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row  # Enable dict-like access
        else:
            # For production databases (PostgreSQL, MySQL, etc.)
            raise NotImplementedError("Add your production database connector here")

        yield conn
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        if conn:
            conn.rollback()
        raise DatabaseError(f"Database operation failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def validate_input(data, required_fields):
    """Validate and sanitize input data"""
    if not data:
        raise BadRequest("No data provided")

    for field in required_fields:
        if field not in data or not data[field]:
            raise BadRequest(f"Missing required field: {field}")

        # Basic input validation
        if not isinstance(data[field], str):
            raise BadRequest(f"Invalid data type for {field}")

        # Length validation
        if len(data[field].strip()) == 0:
            raise BadRequest(f"Empty value for {field}")

        if len(data[field]) > 255:  # Reasonable length limit
            raise BadRequest(f"Value too long for {field}")

    return {k: data[k].strip() for k in required_fields}


def validate_username(username):
    """Validate username format and security"""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if len(username) > 50:
        return False, "Username must be less than 50 characters"

    # Allow alphanumeric and safe special characters
    allowed_chars = set(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
    )
    if not set(username).issubset(allowed_chars):
        return False, "Username contains invalid characters"

    return True, "Valid username"


def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 128:
        return False, "Password too long"

    # Check for basic complexity
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    if not (has_upper and has_lower and has_digit):
        return (
            False,
            "Password must contain uppercase, lowercase, and numeric characters",
        )

    return True, "Valid password"


def hash_password(password):
    """Securely hash password using bcrypt"""
    # Generate salt and hash password
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    return password_hash


def verify_password(password, password_hash):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)


@app.errorhandler(400)
def bad_request(error):
    """Handle bad requests without exposing internal details"""
    logger.warning(f"Bad request: {error.description}")
    return jsonify({"error": "Invalid request", "message": str(error.description)}), 400


@app.errorhandler(401)
def unauthorized(error):
    """Handle unauthorized requests"""
    logger.warning("Unauthorized access attempt")
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit exceeded"""
    logger.warning(f"Rate limit exceeded: {get_remote_address()}")
    return (
        jsonify({"error": "Rate limit exceeded", "message": "Too many requests"}),
        429,
    )


@app.errorhandler(500)
def internal_error(error):
    """Handle internal errors without exposing details"""
    logger.error(f"Internal error: {error}")
    return jsonify({"error": "Internal server error"}), 500


@app.route("/health")
def health_check():
    """Health check endpoint without sensitive information"""
    try:
        # Test database connection
        with get_db_connection() as conn:
            conn.execute("SELECT 1").fetchone()

        return jsonify(
            {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0",
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return (
            jsonify(
                {"status": "unhealthy", "timestamp": datetime.utcnow().isoformat()}
            ),
            503,
        )


@app.route("/users", methods=["GET"])
@limiter.limit("10 per minute")
def get_users():
    """Get list of users (without sensitive information)"""
    try:
        with get_db_connection() as conn:
            users = conn.execute(
                "SELECT id, username, created_at FROM users ORDER BY created_at DESC"
            ).fetchall()

        user_list = [
            {
                "id": user["id"],
                "username": user["username"],
                "created_at": user["created_at"],
            }
            for user in users
        ]

        logger.info(f"Retrieved {len(user_list)} users")
        return jsonify({"users": user_list})

    except DatabaseError as e:
        logger.error(f"Database error in get_users: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in get_users: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/users", methods=["POST"])
@limiter.limit("5 per minute")  # Stricter rate limiting for user creation
def create_user():
    """Create a new user with security validations"""
    try:
        # Validate input data
        data = validate_input(request.get_json(), ["username", "password"])
        username = data["username"]
        password = data["password"]

        # Validate username
        username_valid, username_msg = validate_username(username)
        if not username_valid:
            return jsonify({"error": username_msg}), 400

        # Validate password
        password_valid, password_msg = validate_password(password)
        if not password_valid:
            return jsonify({"error": password_msg}), 400

        # Hash password securely
        password_hash = hash_password(password)

        with get_db_connection() as conn:
            # Check if username already exists
            existing_user = conn.execute(
                "SELECT id FROM users WHERE username = ?", (username,)
            ).fetchone()

            if existing_user:
                return jsonify({"error": "Username already exists"}), 400

            # Insert new user with parameterized query
            cursor = conn.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, password_hash, datetime.utcnow().isoformat()),
            )
            user_id = cursor.lastrowid
            conn.commit()

        # Log successful creation (without sensitive data)
        logger.info(f"User created successfully: username={username}, id={user_id}")

        return (
            jsonify(
                {
                    "message": "User created successfully",
                    "user_id": user_id,
                    "username": username,
                }
            ),
            201,
        )

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except DatabaseError as e:
        logger.error(f"Database error in create_user: {e}")
        return jsonify({"error": "User creation failed"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in create_user: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/login", methods=["POST"])
@limiter.limit("10 per minute")  # Rate limiting for login attempts
def login():
    """User authentication with secure practices"""
    try:
        # Validate input data
        data = validate_input(request.get_json(), ["username", "password"])
        username = data["username"]
        password = data["password"]

        with get_db_connection() as conn:
            # Use parameterized query to prevent SQL injection
            user = conn.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,),
            ).fetchone()

        # Verify user exists and password is correct
        if user and verify_password(password, user["password_hash"]):
            logger.info(f"Successful login: username={username}")
            return jsonify(
                {
                    "message": "Login successful",
                    "user_id": user["id"],
                    "username": user["username"],
                }
            )
        else:
            # Generic error message to prevent username enumeration
            logger.warning(f"Failed login attempt: username={username}")
            return jsonify({"error": "Invalid credentials"}), 401

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except DatabaseError as e:
        logger.error(f"Database error in login: {e}")
        return jsonify({"error": "Authentication failed"}), 500
    except Exception as e:
        logger.error(f"Unexpected error in login: {e}")
        return jsonify({"error": "Internal server error"}), 500


def init_db():
    """Initialize database with proper error handling"""
    try:
        with get_db_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash BLOB NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Create index for performance
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)"
            )

            conn.commit()
            logger.info("Database initialized successfully")

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise DatabaseError(f"Failed to initialize database: {e}")


if __name__ == "__main__":
    try:
        # Initialize database
        init_db()

        # Get configuration from environment
        debug_mode = os.environ.get("FLASK_ENV") == "development"
        port = int(os.environ.get("PORT", 5000))
        host = os.environ.get("HOST", "127.0.0.1")

        logger.info(
            f"Starting Flask app in {'debug' if debug_mode else 'production'} mode"
        )
        app.run(host=host, port=port, debug=debug_mode)

    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
