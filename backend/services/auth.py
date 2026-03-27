import jwt
import datetime
import os
from functools import wraps
from flask import request, jsonify

# Load from environment or config
try:
    from ..config import Config
    SECRET_KEY = Config.JWT_SECRET_KEY
    JWT_ALGORITHM = Config.JWT_ALGORITHM
    JWT_EXPIRATION_HOURS = Config.JWT_EXPIRATION_HOURS
except (ImportError, RuntimeError):
    # Fallback for development
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-key-change-this")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 2


def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "Token missing"}), 401

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error": "Invalid token format"}), 401

        user_id = verify_token(token)

        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        request.user_id = user_id
        return f(*args, **kwargs)

    return decorated