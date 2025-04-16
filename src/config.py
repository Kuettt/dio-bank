import os

class Config:
    TESTING = False
    SECRET_KEY=os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    print("ENTRANDO NO MODO DESENVOLVEDOR...")
    SECRET_KEY="dev"
    SQLALCHEMY_DATABASE_URI="sqlite:///blog.sqlite"
    JWT_SECRET_KEY = "super-secret"



class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "test"
    DATABASE_URI = 'sqlite://'
    JWT_SECRET_KEY = 'test'