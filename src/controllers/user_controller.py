import src.views
from sqlalchemy import inspect
from flask import Blueprint, request, render_template
from src.app import User, db
from http import HTTPStatus
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils import require_permission

app = Blueprint("user", __name__, url_prefix="/users")

def _create_user():
    data = request.json
    user = User(
       username=data["username"],
       password=data["password"],
       role_id=data["role_id"]
    ) 

    db.session.add(user)
    db.session.commit()
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [{'id':user.id,
             'username':user.username,
             'role': {
                 "id": user.role.id,
                 "name": user.role.name
             }
            } 
            for user in users
            
         ]


@app.route("/", methods=["GET", "POST"])
@jwt_required()
@require_permission("admin")
def list_create_users():

    if request.method == "POST":
        _create_user()
        return {"message": "User created"}, HTTPStatus.CREATED
    else:
        return {"user":_list_users()}

@app.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return [{"id": user_id, "name": user.username, "active": user.active}]

@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    mapper = inspect(User)

    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    
    db.session.commit() 
    return [{"id": user_id, "username": user.username, "active": user.active}]

@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT