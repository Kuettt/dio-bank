from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.models import *
from src.utils import required_permission
from http import HTTPStatus  
from src.views.post_schema import PostSchema, CreatePostSchema
from marshmallow import ValidationError

app = Blueprint("post", __name__, url_prefix="/posts")


def _create_post():

    post_schema = CreatePostSchema()


    try:
        user_id = get_jwt_identity()
        query = db.select(User.username)
        user_username = db.session.execute(query.where(User.id == user_id)).scalar()       
        data = post_schema.load(request.json, many=False)
     
    except ValidationError as exc:
        return exc.messages , HTTPStatus.UNPROCESSABLE_CONTENT



    post = Post(title=data["title"],
                body=data["body"], 
                created=datetime.now(),
                author_id=user_id, 
                author=user_username
                )


    db.session.add(post)
    db.session.commit()
    return post_schema.dump(post)

def _list_posts():
    posts = db.session.execute(db.select(Post)).scalars()
    posts_schema = PostSchema()
    return posts_schema.dump(posts, many=True)


@app.route("/", methods=["GET", "POST"])
@jwt_required()
def handle_post():
    
    if request.method == "POST":
        _create_post()
        return _create_post()

    else:
        return {"posts": _list_posts()}


@app.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
@required_permission("admin")
def delete_post(post_id:int):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT



@app.route("/<int:post_id>", methods=["PATCH"])
@jwt_required()
@required_permission("admin")
def update_post(post_id):

    post = db.get_or_404(Post, post_id)
    
    data = request.json

    allowed_fields = {"title", "body"}

    for field in allowed_fields:
        if field in allowed_fields:
            setattr(post, field, data[field])

    db.session.commit()
    return [{'id': post_id,'user':post.author, "title":post.title, "body":post.body, "created_at":post.created.strftime("%d/%m/%Y %H:%M")}]