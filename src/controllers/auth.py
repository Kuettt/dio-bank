import src.views
from flask import jsonify
from flask import Blueprint, request
from src.models import *
from src.app import bcrypt
from http import HTTPStatus
from flask_jwt_extended import create_access_token

app = Blueprint("auth", __name__, url_prefix="/auth")

def _valid_password(password_hash, password_raw):
    result = bcrypt.check_password_hash(password_hash, password_raw)
    return result

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username =  data["username"]
    password = data["password"]
    #busca o nome informado no banco de dados
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or not _valid_password(user.password, password):
        return jsonify({"msg": "Bad username or password"}), HTTPStatus.UNAUTHORIZED
    
    user_id = str(user.id)
    access_token = create_access_token(identity=user_id)
    return {"access_token": access_token}
