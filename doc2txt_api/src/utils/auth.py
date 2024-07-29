import os
import jwt
from flask import (
    request,
    jsonify
)
from functools import wraps
from utils.exceptions import AccessDenied


def _jwt_validation(token: str) -> dict:
    """JWT validation"""
    try:
        return jwt.decode(
            token,
            os.getenv('JWT_KEY'),
            algorithms=['HS512']
            )
    except jwt.ExpiredSignatureError:
        raise AccessDenied('Signature expired.')
    except jwt.InvalidTokenError:
        raise AccessDenied('Invalid token.')


def _is_authorized(headers: dict) -> None:
    """Auth manager"""
    if headers.get('Authorization'):
        token = headers.get('Authorization').split()[1]
        _ = _jwt_validation(token)
    else:
        raise AccessDenied('Invalid auth method.')


def my_auth(f):
    """Auth decorator"""
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            _is_authorized(request.headers)
        except AccessDenied as e:
            return jsonify({'error': str(e)}), 403
        return f(*args, **kwargs)

    return inner
