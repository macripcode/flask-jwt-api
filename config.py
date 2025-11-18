import os
from urllib.parse import quote_plus

def _build_uri():
    uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    if uri:
        return uri

    engine = os.getenv("DB_ENGINE")

 
    if not engine or engine == "sqlite":
        name = os.getenv("DB_NAME", "sqlite.db")
        return f"sqlite:///{name}"

    user = os.getenv("DB_USER", "admin")
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "flaskenv")

    return f"{engine}://{user}:{password}@{host}:{port}/{name}"

class Base:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    PROPAGATE_EXCEPTIONS = True

class Dev(Base):
    SQLALCHEMY_DATABASE_URI = _build_uri()

class Prod(Base):
    SQLALCHEMY_DATABASE_URI = _build_uri()
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

def get_config(env: str):
    return {"development": Dev, "production": Prod}.get(env, Dev)
