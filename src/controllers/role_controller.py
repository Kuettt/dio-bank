from flask import Blueprint, request
from src.models import *
from src.utils import required_permission
from flask_jwt_extended import jwt_required
from http import HTTPStatus

app = Blueprint("role", __name__, url_prefix="/roles")

@jwt_required()
@required_permission("admin")
def _delete_role(id):
    role = db.get_or_404(Role, id)
        
    db.session.delete(role)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT

@jwt_required()
@required_permission("admin")
def _create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {'message': 'role created'}, HTTPStatus.CREATED




@app.route("/", methods=["POST"])
def create_role():
    return _create_role()

@app.route("/<int:role_id>", methods=["DELETE"])
def delete_role(role_id:int):
    _delete_role(role_id)
    return "", HTTPStatus.NO_CONTENT
