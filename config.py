import os

class Base:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    PROPAGATE_EXCEPTIONS = True

class Dev(Base):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///instance/app.db")

class Prod(Base):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

def get_config(env: str):
    return {"development": Dev, "production": Prod}.get(env, Dev)
