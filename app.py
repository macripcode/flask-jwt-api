import os
from flask import Flask
from config import get_config
from extensions import db, jwt, cors
from utils.errors import register_error_handlers
from api.auth import bp as auth_bp
from api.products import bp as products_bp
from api.status import bp as status_bp
from models.user import User
from models.product import Product

from sqlalchemy.exc import IntegrityError


def create_app(env: str | None = None):
    env = env or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(status_bp)

    register_error_handlers(app)

    with app.app_context():
        os.makedirs("/app/instance", exist_ok=True)
        db.create_all()
        if os.getenv("SEED_ADMIN") == "1":
            email = os.getenv("ADMIN_EMAIL", "admin@local")
            pwd = os.getenv("ADMIN_PASSWORD", "admin")
            try:
                if not User.query.filter_by(email=email).first():
                    u = User(email=email)
                    u.set_password(pwd)
                    db.session.add(u)
                    db.session.commit()
            except IntegrityError:
                db.session.rollback()

    return app

app = create_app()
