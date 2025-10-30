from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User

bp = Blueprint("auth", __name__)

@bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password", "")
    if not email:
        return jsonify({"msg": "email required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Bad credentials"}), 401

    # identity como STRING (id o email) + claims extra
    token = create_access_token(
        identity=str(user.id),  # <-- clave: string
        additional_claims={
            "email": user.email,
            "role": user.role
        }
    )
    return jsonify({"access_token": token}), 200