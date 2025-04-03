
from sqlalchemy import inspect
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.app import Post, db, User
from src.utils import require_permission
from http import HTTPStatus  

app = Blueprint("post", __name__, url_prefix="/posts")


def _create_post():
    data = request.json
    user_id = get_jwt_identity()
    user_username = db.session.execute(db.select(User.username).where(User.id == user_id)).scalar() 
    post = Post(title=data["title"], body=data["body"], created=datetime.now(), author_id=user_id, author=user_username)
    db.session.add(post)
    db.session.commit()


def _list_posts():
    posts = db.session.execute(db.select(Post)).scalars()
    
    
    return[{'id': post.id,'user':post.author, "title":post.title, "body":post.body, "created_at":post.created.strftime("%d/%m/%Y %H:%M")} for post in posts]

@app.route("/", methods=["GET", "POST"])
@jwt_required()
def handle_post():
    
    if request.method == "POST":
        _create_post()
        return {"message": "Postagem enviada"}, HTTPStatus.CREATED

    else:
        return {"Post": _list_posts()}


@app.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
@require_permission("admin")
def delete_post(post_id:int):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT



@app.route("/<int:post_id>", methods=["PATCH"])
@jwt_required()
@require_permission("admin")
def update_post(post_id):

    post = db.get_or_404(Post, post_id)
    
    data = request.json

    allowed_fields = {"title", "body"}

    for field in allowed_fields:
        if field in allowed_fields:
            setattr(post, field, data[field])

    db.session.commit()
    return [{'id': post_id,'user':post.author, "title":post.title, "body":post.body, "created_at":post.created.strftime("%d/%m/%Y %H:%M")}]