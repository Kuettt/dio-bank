
from sqlalchemy import inspect
from flask import Blueprint, request
from datetime import datetime
from src.app import Post, db
from http import HTTPStatus  

app = Blueprint("post", __name__, url_prefix="/posts")


def _create_post():
    data = request.json
    post = Post(title=data["title"], body=data["body"], created=datetime.now(), author_id=data["autor_id"])
    db.session.add(post)
    db.session.commit()


def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return[{'id':post.id, "title":post.title, "body":post.body} for post in posts]

@app.route("/", methods=["GET", "POST"])
def handle_post():
    
    if request.method == "POST":
        _create_post()
        return {"message": "Postagem enviada"}, HTTPStatus.CREATED

    else:
        return {"Post": _list_posts()}
