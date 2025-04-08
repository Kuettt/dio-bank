import os
from datetime import datetime

import click
import sqlalchemy as sa
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate= Migrate()
jwt = JWTManager()

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.username!r})"

class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(sa.String, nullable=True, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped["Role"] = relationship(back_populates="user")
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, active={self.active!r})"


class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, default=lambda:datetime.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    author: Mapped[str] = mapped_column(sa.ForeignKey("user.username"))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, title={self.title}, author={self.author}, author_id={self.author_id})"

@click.command("init-db")
def init_db_command():
    # pois o db está pra fora da função, então existe a necessidade de chama-lo como global
    global db
    with current_app.app_context():
        db.create_all()
        click.echo("O banco de dados foi criado com sucesso!")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev", 
        SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
        JWT_SECRET_KEY = "super-secret",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.cli.add_command(init_db_command)
    # initializng flask sql-alchemy instance
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    #importanções de controllers devem ficar dentro do create_app
    from src.controllers import user_controller, post_controller, auth, role_controller
    
    app.register_blueprint(user_controller.app)
    app.register_blueprint(post_controller.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role_controller.app)
    return app
