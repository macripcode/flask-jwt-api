# api/status.py
from flask import Blueprint, jsonify

bp = Blueprint("status", __name__)

@bp.get("/health")
def health():
    return jsonify({"status": "ok"}), 200