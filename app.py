from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
import copy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

SOFAS = [
    {
        "id": "sofa_1",
        "type": "sofa",
        "name": "Modern 3-Seater Sofa",
        "price": 700,
        "dimensions": "84 W x 35 D x 34 H in",
        "rating": 4.5,
        "reviews": 1284,
        "purchases": 3200,
        "in_stock": True,
        "material": "Solid wood frame, polyester upholstery",
        "brand": "SmartLiving",
        "color": "Gray",
        "images": {
            "front": "/assets/items/sofa/sofa1.webp",
            "left": "/assets/items/sofa/sofa1.webp",
            "right": "/assets/items/sofa/sofa1.webp",
        },
        "positions": {
            "front": {"x": 110, "y": 275, "width": 300, "height": 150},
            "left": {"x": 130, "y": 270, "width": 260, "height": 150},
            "right": {"x": 500, "y": 270, "width": 260, "height": 150},
        },
    },
    {
        "id": "sofa_2",
        "type": "sofa",
        "name": "Beige Sectional Sofa",
        "price": 920,
        "dimensions": "102 W x 64 D x 35 H in",
        "rating": 4.6,
        "reviews": 842,
        "purchases": 2100,
        "in_stock": True,
        "material": "Engineered wood, linen blend upholstery",
        "brand": "CasaForm",
        "color": "Beige",
        "images": {
            "front": "/assets/items/sofa/sofa2.jpg",
            "left": "/assets/items/sofa/sofa2.jpg",
            "right": "/assets/items/sofa/sofa2.jpg",
        },
        "positions": {
            "front": {"x": 95, "y": 265, "width": 330, "height": 165},
            "left": {"x": 115, "y": 258, "width": 285, "height": 165},
            "right": {"x": 475, "y": 258, "width": 285, "height": 165},
        },
    },
    {
        "id": "sofa_3",
        "type": "sofa",
        "name": "Compact Sofa",
        "price": 640,
        "dimensions": "76 W x 33 D x 32 H in",
        "rating": 4.3,
        "reviews": 615,
        "purchases": 1700,
        "in_stock": False,
        "material": "Rubberwood legs, woven fabric",
        "brand": "UrbanNest",
        "color": "Blue",
        "images": {
            "front": "/assets/items/sofa/sofa3.webp",
            "left": "/assets/items/sofa/sofa3.webp",
            "right": "/assets/items/sofa/sofa3.webp",
        },
        "positions": {
            "front": {"x": 125, "y": 285, "width": 260, "height": 135},
            "left": {"x": 145, "y": 280, "width": 235, "height": 135},
            "right": {"x": 520, "y": 280, "width": 235, "height": 135},
        },
    },
]

CENTER_TABLES = [
    {
        "id": "table_1",
        "type": "center_table",
        "name": "Wood Center Table",
        "price": 250,
        "dimensions": "42 W x 22 D x 18 H in",
        "rating": 4.4,
        "reviews": 903,
        "purchases": 2600,
        "in_stock": True,
        "material": "Mango wood with matte finish",
        "brand": "OakLine",
        "color": "Walnut",
        "images": {
            "front": "/assets/items/tables/table1.webp",
            "left": "/assets/items/tables/table1.webp",
            "right": "/assets/items/tables/table1.webp",
        },
        "positions": {
            "front": {"x": 425, "y": 315, "width": 150, "height": 95},
            "left": {"x": 425, "y": 320, "width": 140, "height": 90},
            "right": {"x": 355, "y": 320, "width": 140, "height": 90},
        },
    },
    {
        "id": "table_2",
        "type": "center_table",
        "name": "Glass Center Table",
        "price": 320,
        "dimensions": "40 W x 24 D x 17 H in",
        "rating": 4.2,
        "reviews": 522,
        "purchases": 1500,
        "in_stock": True,
        "material": "Tempered glass top, steel frame",
        "brand": "ClearHome",
        "color": "Clear",
        "images": {
            "front": "/assets/items/tables/table2.jpg",
            "left": "/assets/items/tables/table2.jpg",
            "right": "/assets/items/tables/table2.jpg",
        },
        "positions": {
            "front": {"x": 430, "y": 318, "width": 145, "height": 90},
            "left": {"x": 430, "y": 320, "width": 135, "height": 86},
            "right": {"x": 360, "y": 320, "width": 135, "height": 86},
        },
    },
    {
        "id": "table_3",
        "type": "center_table",
        "name": "Marble Top Center Table",
        "price": 410,
        "dimensions": "44 W x 24 D x 17 H in",
        "rating": 4.7,
        "reviews": 311,
        "purchases": 980,
        "in_stock": True,
        "material": "Engineered marble top, metal base",
        "brand": "LuxeNest",
        "color": "White",
        "images": {
            "front": "/assets/items/tables/table3.webp",
            "left": "/assets/items/tables/table3.webp",
            "right": "/assets/items/tables/table3.webp",
        },
        "positions": {
            "front": {"x": 420, "y": 312, "width": 160, "height": 96},
            "left": {"x": 420, "y": 318, "width": 145, "height": 90},
            "right": {"x": 350, "y": 318, "width": 145, "height": 90},
        },
    },
]

TV_STANDS = [
    {
        "id": "tv_1",
        "type": "tv_stand",
        "name": "Minimal TV Stand",
        "price": 300,
        "dimensions": "58 W x 16 D x 22 H in",
        "rating": 4.5,
        "reviews": 1130,
        "purchases": 2900,
        "in_stock": True,
        "material": "Engineered wood with laminate finish",
        "brand": "ViewCraft",
        "color": "Oak",
        "images": {
            "front": "/assets/items/tvstands/tvstand1.webp",
            "left": "/assets/items/tvstands/tvstand1.webp",
            "right": "/assets/items/tvstands/tvstand1.webp",
        },
        "positions": {
            "front": {"x": 640, "y": 170, "width": 210, "height": 110},
            "left": {"x": 700, "y": 182, "width": 150, "height": 92},
            "right": {"x": 70, "y": 182, "width": 150, "height": 92},
        },
    },
    {
        "id": "tv_2",
        "type": "tv_stand",
        "name": "Floating TV Stand",
        "price": 360,
        "dimensions": "60 W x 14 D x 16 H in",
        "rating": 4.3,
        "reviews": 744,
        "purchases": 1850,
        "in_stock": True,
        "material": "MDF, wall-mount hardware included",
        "brand": "SkyWall",
        "color": "Black",
        "images": {
            "front": "/assets/items/tvstands/tvstand2.jpg",
            "left": "/assets/items/tvstands/tvstand2.jpg",
            "right": "/assets/items/tvstands/tvstand2.jpg",
        },
        "positions": {
            "front": {"x": 645, "y": 172, "width": 205, "height": 100},
            "left": {"x": 705, "y": 185, "width": 145, "height": 88},
            "right": {"x": 75, "y": 185, "width": 145, "height": 88},
        },
    },
    {
        "id": "tv_3",
        "type": "tv_stand",
        "name": "Classic TV Cabinet",
        "price": 480,
        "dimensions": "64 W x 18 D x 24 H in",
        "rating": 4.6,
        "reviews": 458,
        "purchases": 1210,
        "in_stock": False,
        "material": "Solid wood frame, veneer finish",
        "brand": "HeritageHome",
        "color": "Espresso",
        "images": {
            "front": "/assets/items/tvstands/tvstand3.jpg",
            "left": "/assets/items/tvstands/tvstand3.jpg",
            "right": "/assets/items/tvstands/tvstand3.jpg",
        },
        "positions": {
            "front": {"x": 635, "y": 168, "width": 215, "height": 112},
            "left": {"x": 700, "y": 180, "width": 150, "height": 94},
            "right": {"x": 70, "y": 180, "width": 150, "height": 94},
        },
    },
]

CATALOG = {
    "sofa": SOFAS,
    "center_table": CENTER_TABLES,
    "tv_stand": TV_STANDS,
}

ROOM = {
    "width": 920,
    "height": 520,
    "angles": ["front", "left", "right"]
}

def pick_one(item_type, exclude_id=None):
    options = [item for item in CATALOG[item_type] if item["id"] != exclude_id]
    return copy.deepcopy(random.choice(options))

def build_design(budget=None):
    items = [
        pick_one("sofa"),
        pick_one("center_table"),
        pick_one("tv_stand"),
    ]
    total = sum(item["price"] for item in items)
    return {
        "room": ROOM,
        "items": items,
        "total": total,
        "within_budget": total <= budget if budget is not None else True
    }

def refresh_totals(design, budget=None):
    total = sum(item["price"] for item in design["items"])
    design["total"] = total
    design["within_budget"] = total <= budget if budget is not None else True
    return design

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "SmartFurnish Backend Running"})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    budget = data.get("budget")
    return jsonify(build_design(budget))

@app.route("/regenerate", methods=["POST"])
def regenerate():
    data = request.get_json() or {}
    budget = data.get("budget")
    return jsonify(build_design(budget))

@app.route("/regenerate-item", methods=["POST"])
def regenerate_item():
    data = request.get_json() or {}
    item_type = data.get("itemType")
    design = copy.deepcopy(data.get("design"))
    budget = data.get("budget")

    if not design or item_type not in CATALOG:
        return jsonify({"error": "Invalid request"}), 400

    for i, item in enumerate(design["items"]):
        if item["type"] == item_type:
            design["items"][i] = pick_one(item_type, exclude_id=item["id"])
            break

    return jsonify(refresh_totals(design, budget))

@app.route("/remove-item", methods=["POST"])
def remove_item():
    data = request.get_json() or {}
    item_type = data.get("itemType")
    design = copy.deepcopy(data.get("design"))
    budget = data.get("budget")

    if not design:
        return jsonify({"error": "Invalid request"}), 400

    design["items"] = [item for item in design["items"] if item["type"] != item_type]
    return jsonify(refresh_totals(design, budget))

@app.route("/update-layout", methods=["POST"])
def update_layout():
    data = request.get_json() or {}
    design = data.get("design")
    budget = data.get("budget")

    if not design:
        return jsonify({"error": "Invalid request"}), 400

    return jsonify(refresh_totals(design, budget))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)