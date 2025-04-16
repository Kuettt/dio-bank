from src.app import ma
from src.models import User
from src.views.role_schema import RoleSchema
from marshmallow import fields

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
    
    id = ma.auto_field()
    username = ma.auto_field()
    role = ma.Nested(RoleSchema)

class UserIdParameter(ma.SQLAlchemySchema):
    user_id = fields.Int(required=True, strict=True)


class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)    
    role_id = fields.Integer(required=True, strict=True)