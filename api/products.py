from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.product import Product
from extensions import db
from utils.pagination import apply_ra_pagination
from sqlalchemy import func

bp = Blueprint("products", __name__)

@bp.get("")
@jwt_required()
def list_products():
    q = Product.query
    items, total = apply_ra_pagination(q, request.args)
    resp = jsonify([{
        "id": p.id,
        "name": p.name, 
        "price": p.price,
        "stock": p.stock, 
        "image_url": p.image_url,
        "category": p.category
    } for p in items])
    resp.headers["X-Total-Count"] = str(total)
    return resp

@bp.get("/<int:pid>")
@jwt_required()
def get_one(pid):
    p = Product.query.get_or_404(pid)
    return jsonify({
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "image_url": p.image_url,
        "category": p.category       
    })

@bp.post("")
@jwt_required()
def create():
    data = request.get_json() or {}
    if "name" not in data or "price" not in data:
        return jsonify({"msg":"name and price are required"}), 400
    p = Product(
        name=data["name"], 
        price=float(data["price"]),
        stock=int(data.get("stock",0)), 
        image_url=data.get("image_url"),
        category=data.get("category")
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
    for f in ["name","price","stock","image_url", "category"]:
        if f in data:
            if f == "price":
                setattr(p, f, float(data[f]))
            elif f == "stock":
                setattr(p, f, int(data[f]))
            else:
                setattr(p, f, data[f])
    db.session.commit()
    return jsonify({
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "image_url": p.image_url,
        "category": p.category,
    })

@bp.delete("/<int:pid>")
@jwt_required()
def delete(pid):
    p = Product.query.get_or_404(pid)
    db.session.delete(p); db.session.commit()
    return jsonify({"deleted": pid})

@bp.get("/search")
@jwt_required()
def search_products():
    q = Product.query

    term = request.args.get("q")
    if term:
        q = q.filter(Product.name.ilike(f"%{term}%"))

    category = request.args.get("category")
    if category:
        q = q.filter(Product.category == category)

    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    if min_price is not None:
        q = q.filter(Product.price >= min_price)
    if max_price is not None:
        q = q.filter(Product.price <= max_price)

    items, total = apply_ra_pagination(q, request.args)

    resp = jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "stock": p.stock,
        "image_url": p.image_url,
        "category": p.category,
    } for p in items])
    resp.headers["X-Total-Count"] = str(total)
    return resp

@bp.get("/categories")
@jwt_required()
def list_categories():
    rows = db.session.query(
        Product.category,
        func.count(Product.id)
    ).group_by(Product.category).all()

    categories = [
        {"name": name, "count": count}
        for name, count in rows
        if name is not None
    ]

    return jsonify(categories)
