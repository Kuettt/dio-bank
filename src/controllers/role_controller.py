from flask import Blueprint, request
from src.app import db
from src.utils import require_permission
from flask_jwt_extended import jwt_required
from src.app import Role
from http import HTTPStatus

app = Blueprint("role", __name__, url_prefix="/roles")

@app.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {'message': 'role created'}, HTTPStatus.CREATED
