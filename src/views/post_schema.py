from src.app import ma
from src.models.post import Post
from src.models.user import User
from marshmallow import fields



class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True



class CreatePostSchema(ma.SQLAlchemySchema):
    title = fields.String(required=True)
    body = fields.String(required=True)
    created = fields.DateTime(dump_only=True)
    author_id = fields.Integer(dump_only=True, strict=True)
    author = fields.String(dump_only=True)

    