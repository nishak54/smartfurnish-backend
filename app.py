from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
import copy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

ROOM_SCENES = {
    "front": "/assets/rooms/livingroom-front.jpg",
    "left": "/assets/rooms/livingroom-left.jpg",
    "right": "/assets/rooms/livingroom-right.jpg",
}

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
            "front": "/assets/items/sofas/sofa-gray-front.png",
            "left": "/assets/items/sofas/sofa-gray-left.png",
            "right": "/assets/items/sofas/sofa-gray-right.png",
        },
        "positions": {
            "front": {"x": 80, "y": 260, "width": 300, "height": 140},
            "left": {"x": 120, "y": 250, "width": 250, "height": 150},
            "right": {"x": 420, "y": 250, "width": 250, "height": 150},
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
            "front": "/assets/items/sofas/sofa-beige-front.png",
            "left": "/assets/items/sofas/sofa-beige-left.png",
            "right": "/assets/items/sofas/sofa-beige-right.png",
        },
        "positions": {
            "front": {"x": 65, "y": 250, "width": 330, "height": 155},
            "left": {"x": 110, "y": 240, "width": 275, "height": 160},
            "right": {"x": 405, "y": 240, "width": 275, "height": 160},
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
            "front": "/assets/items/tables/table-wood-front.png",
            "left": "/assets/items/tables/table-wood-left.png",
            "right": "/assets/items/tables/table-wood-right.png",
        },
        "positions": {
            "front": {"x": 430, "y": 300, "width": 150, "height": 90},
            "left": {"x": 410, "y": 300, "width": 140, "height": 85},
            "right": {"x": 350, "y": 300, "width": 140, "height": 85},
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
            "front": "/assets/items/tables/table-glass-front.png",
            "left": "/assets/items/tables/table-glass-left.png",
            "right": "/assets/items/tables/table-glass-right.png",
        },
        "positions": {
            "front": {"x": 425, "y": 302, "width": 150, "height": 88},
            "left": {"x": 405, "y": 302, "width": 135, "height": 84},
            "right": {"x": 355, "y": 302, "width": 135, "height": 84},
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
            "front": "/assets/items/tvstands/tvstand-oak-front.png",
            "left": "/assets/items/tvstands/tvstand-oak-left.png",
            "right": "/assets/items/tvstands/tvstand-oak-right.png",
        },
        "positions": {
            "front": {"x": 610, "y": 145, "width": 220, "height": 120},
            "left": {"x": 650, "y": 150, "width": 180, "height": 105},
            "right": {"x": 90, "y": 150, "width": 180, "height": 105},
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
            "front": "/assets/items/tvstands/tvstand-black-front.png",
            "left": "/assets/items/tvstands/tvstand-black-left.png",
            "right": "/assets/items/tvstands/tvstand-black-right.png",
        },
        "positions": {
            "front": {"x": 615, "y": 150, "width": 220, "height": 105},
            "left": {"x": 655, "y": 155, "width": 175, "height": 96},
            "right": {"x": 95, "y": 155, "width": 175, "height": 96},
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
    "angles": ROOM_SCENES,
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