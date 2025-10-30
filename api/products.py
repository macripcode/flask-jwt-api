from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.product import Product
from extensions import db
from utils.pagination import apply_ra_pagination

bp = Blueprint("products", __name__)

@bp.get("")
@jwt_required()
def list_products():
    q = Product.query
    items, total = apply_ra_pagination(q, request.args)
    resp = jsonify([{
        "id": p.id, "name": p.name, "price": p.price,
        "stock": p.stock, "image_url": p.image_url
    } for p in items])
    resp.headers["X-Total-Count"] = str(total)
    return resp

@bp.get("/<int:pid>")
@jwt_required()
def get_one(pid):
    p = Product.query.get_or_404(pid)
    return jsonify({
        "id": p.id, "name": p.name, "price": p.price,
        "stock": p.stock, "image_url": p.image_url
    })

@bp.post("")
@jwt_required()
def create():
    data = request.get_json() or {}
    if "name" not in data or "price" not in data:
        return jsonify({"msg":"name and price are required"}), 400
    p = Product(
        name=data["name"], price=float(data["price"]),
        stock=int(data.get("stock",0)), image_url=data.get("image_url")
    )
    db.session.add(p); db.session.commit()
    return jsonify({
        "id": p.id, "name": p.name, "price": p.price,
        "stock": p.stock, "image_url": p.image_url
    }), 201

@bp.put("/<int:pid>")
@jwt_required()
def update(pid):
    p = Product.query.get_or_404(pid)
    data = request.get_json() or {}
    for f in ["name","price","stock","image_url"]:
        if f in data:
            if f == "price":
                setattr(p, f, float(data[f]))
            elif f == "stock":
                setattr(p, f, int(data[f]))
            else:
                setattr(p, f, data[f])
    db.session.commit()
    return jsonify({
        "id": p.id, "name": p.name, "price": p.price,
        "stock": p.stock, "image_url": p.image_url
    })

@bp.delete("/<int:pid>")
@jwt_required()
def delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p); db.session.commit()
    return jsonify({"deleted": pid})
