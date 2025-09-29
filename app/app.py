from flask import Flask, request, jsonify, abort
from models import get_db, init_db, Product
import os

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgres@db:5432/products")
app.config['DATABASE_URL'] = DATABASE_URL

# Initialize DB on startup (safe for dev: creates table if not exists)
#with app.app_context():
 #   init_db(app.config['DATABASE_URL'])

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/products", methods=["GET"])
def list_products():
    products = Product.list_all(app.config['DATABASE_URL'])
    return jsonify([p.to_dict() for p in products]), 200

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    p = Product.get_by_id(app.config['DATABASE_URL'], product_id)
    if not p:
        abort(404)
    return jsonify(p.to_dict()), 200

@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json() or {}
    name = data.get("name")
    price = data.get("price")
    if not name or price is None:
        return jsonify({"error":"name and price required"}), 400
    p = Product.create(app.config['DATABASE_URL'], name, float(price))
    return jsonify(p.to_dict()), 201

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    data = request.get_json() or {}
    p = Product.update(app.config['DATABASE_URL'], product_id, data.get("name"), data.get("price"))
    if not p:
        abort(404)
    return jsonify(p.to_dict()), 200

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    ok = Product.delete(app.config['DATABASE_URL'], product_id)
    if not ok:
        abort(404)
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
