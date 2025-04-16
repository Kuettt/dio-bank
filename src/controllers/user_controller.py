from sqlalchemy import inspect
from flask import Blueprint, request 
from src.models import *
from http import HTTPStatus
from src.app import bcrypt
from src.views.user_schema import UserSchema, CreateUserSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required
from src.utils import required_permission

app = Blueprint("user", __name__, url_prefix="/users")

def _create_user():
    
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json, many=False)

    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    user = User(
       username=data["username"],
       password=bcrypt.generate_password_hash(data["password"]),
       role_id=data["role_id"]
    ) 

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user)

@jwt_required()
@required_permission("admin")
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    user_schema = UserSchema()
    return user_schema.dump(users,many=True)


@app.route("/", methods=["GET", "POST"])
def list_create_users():

    if request.method == "POST":
        return _create_user()
        
    else:
        return {"user":_list_users()}

@app.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """User detail view.
    ---
    get:
      tags:
        - user
      parameters:
        - in: path
          name: user_id
          schema: UserIdParameter 
      responses:
        200:
          description: Successful operation
          content:
            application/json:
              schema: UserSchema
          
        
    """   
    user = db.get_or_404(User, user_id)
    user_schema = UserSchema()
    return user_schema.dump(user)

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
    """User detail view.
    ---
    delete:
      tags:
        - user
      parameters:
        - in: path
          name: user_id
          schema: UserIdParameter 
      responses:
        204:
          description: Delete a user
          content:
            application/json:
              schema: UserSchema
        404:
          description: Not found user
          
        
    """  
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT