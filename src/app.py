import os
from datetime import datetime

import sqlalchemy as sa
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models.base import db
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

class Base(DeclarativeBase):
    pass

migrate= Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()
spec = APISpec(
    title="DIO Bank",
    version="1.0.0",
    openapi_version = "3.0.4",
    info=dict(description="DIO Bank API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


def create_app(environment=os.environ['ENVIRONMENT']):
    app = Flask(__name__, instance_relative_config=True)
   
    app.config.from_object(f"src.config.{environment.title()}Config")
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #Inicializated extension
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    #registrated blueprints
    from src.controllers import user_controller, post_controller, auth, role_controller
    app.register_blueprint(user_controller.app)
    app.register_blueprint(post_controller.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role_controller.app)

    @app.route("/docs")
    def docs():
        return spec.path(view=user_controller.delete_user).path(view=user_controller.get_user).to_dict()

    #exceptions returns
    from werkzeug.exceptions import HTTPException
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"
        return response

    return app
