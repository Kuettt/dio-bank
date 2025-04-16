from flask_jwt_extended import get_jwt_identity
from src.models import *
from http import HTTPStatus
from functools import wraps

def required_permission(role_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            user = db.session.execute(db.select(User).where(User.id == identity)).scalar()
        
            if not user:
                return {"message": "User not found"}, HTTPStatus.NOT_FOUND

            if user.role.name != role_name:
                return {"message": "User don't have access!"}, HTTPStatus.FORBIDDEN
        
            return f(*args, **kwargs)

        return wrapper
    
    return decorator


def eleva_quadrado(x):
    return x**2