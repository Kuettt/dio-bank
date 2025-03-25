import src.views
from flask import jsonify
from sqlalchemy import inspect
from flask import Blueprint, request, render_template
from src.app import User, db
from http import HTTPStatus
from werkzeug.security import generate_password_hash

from flask_jwt_extended import create_access_token, get_jwt_identity


app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username =  data["username"]
    password = data["password"]
    #busca o nome informado no banco de dados
    user = db.session.execute(db.select(User).where(User.username == username, User.password == password)).scalar()
    if not user:
        return jsonify({"msg": "Bad username or password"}), HTTPStatus.UNAUTHORIZED
    
    user_id = str(user.id)
    access_token = create_access_token(identity=user_id)
    return {"access_token": access_token}
