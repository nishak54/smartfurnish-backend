from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# =========================
# LOAD PRODUCT DATASET
# =========================
with open("products.json", "r") as f:
    PRODUCTS = json.load(f)

# =========================
# FILTER FUNCTION
# =========================
def get_products_by_category(category, budget):
    results = []

    for product in PRODUCTS:
        if product["category"] == category and product["price"] <= budget:
            results.append(product)

    # Sort by price (cheapest first)
    results.sort(key=lambda x: x["price"])

    return results[:3]


# =========================
# API ENDPOINT
# =========================
@app.route("/api/get_items", methods=["POST"])
def get_items():
    data = request.json

    budget = data.get("budget", 0)
    room = data.get("room", "living_room")

    if room != "living_room":
        return jsonify({"error": "Only living room supported"}), 400

    return jsonify({
        "sofa": get_products_by_category("sofa", budget),
        "coffee_table": get_products_by_category("coffee_table", budget),
        "tv_stand": get_products_by_category("tv_stand", budget)
    })


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))