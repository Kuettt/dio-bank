from flask_jwt_extended import get_jwt_identity
from src.app import db, User
from http import HTTPStatus
from functools import wraps

def require_permission(role_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            user = db.get_or_404(User, identity)
        
            if user.role.name != role_name:
                return {"message": "User don't have access!"}, HTTPStatus.FORBIDDEN
        
            return f(*args, **kwargs)

        return wrapper
    
    return decorator


def eleva_quadrado(x):
    return x**2