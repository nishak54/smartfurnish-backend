from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
import urllib.parse
import copy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def svg_data_uri(label, bg="#e5e7eb", fg="#111827", accent="#9ca3af"):
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180">
      <rect x="0" y="0" width="320" height="180" rx="18" fill="{bg}"/>
      <rect x="18" y="18" width="284" height="144" rx="14" fill="{accent}" opacity="0.18"/>
      <text x="160" y="98" font-family="Arial, sans-serif" font-size="26" text-anchor="middle" fill="{fg}">{label}</text>
    </svg>
    """
    return "data:image/svg+xml;charset=UTF-8," + urllib.parse.quote(svg)

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
        "image": svg_data_uri("Sofa", "#dbeafe", "#1e3a8a", "#60a5fa"),
        "position": {"x": 70, "y": 230, "width": 260, "height": 120}
    },
    {
        "id": "sofa_2",
        "type": "sofa",
        "name": "L-Shaped Sectional Sofa",
        "price": 920,
        "dimensions": "102 W x 64 D x 35 H in",
        "rating": 4.6,
        "reviews": 842,
        "purchases": 2100,
        "in_stock": True,
        "material": "Engineered wood, linen blend upholstery",
        "brand": "CasaForm",
        "color": "Beige",
        "image": svg_data_uri("Sectional Sofa", "#fef3c7", "#92400e", "#f59e0b"),
        "position": {"x": 55, "y": 215, "width": 290, "height": 135}
    },
    {
        "id": "sofa_3",
        "type": "sofa",
        "name": "Compact Fabric Sofa",
        "price": 640,
        "dimensions": "76 W x 33 D x 32 H in",
        "rating": 4.3,
        "reviews": 615,
        "purchases": 1700,
        "in_stock": False,
        "material": "Rubberwood legs, woven fabric",
        "brand": "UrbanNest",
        "color": "Blue",
        "image": svg_data_uri("Compact Sofa", "#ede9fe", "#5b21b6", "#8b5cf6"),
        "position": {"x": 85, "y": 235, "width": 240, "height": 110}
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
        "image": svg_data_uri("Center Table", "#dcfce7", "#166534", "#22c55e"),
        "position": {"x": 390, "y": 245, "width": 170, "height": 90}
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
        "image": svg_data_uri("Glass Table", "#e0f2fe", "#075985", "#38bdf8"),
        "position": {"x": 390, "y": 248, "width": 165, "height": 85}
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
        "image": svg_data_uri("Marble Table", "#f3f4f6", "#111827", "#9ca3af"),
        "position": {"x": 385, "y": 246, "width": 175, "height": 88}
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
        "image": svg_data_uri("TV Stand", "#fee2e2", "#991b1b", "#f87171"),
        "position": {"x": 610, "y": 80, "width": 230, "height": 110}
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
        "image": svg_data_uri("Floating Stand", "#fce7f3", "#9d174d", "#ec4899"),
        "position": {"x": 615, "y": 88, "width": 225, "height": 100}
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
        "image": svg_data_uri("TV Cabinet", "#ede9fe", "#4c1d95", "#a78bfa"),
        "position": {"x": 605, "y": 78, "width": 240, "height": 118}
    },
]

CATALOG = {
    "sofa": SOFAS,
    "center_table": CENTER_TABLES,
    "tv_stand": TV_STANDS,
}

ROOM = {
    "width": 900,
    "height": 500,
    "background": "linear-gradient(180deg, #faf7f2 0%, #f5efe6 68%, #e7dccd 68%, #e7dccd 100%)"
}

def pick_one(item_type, exclude_id=None):
    options = [item for item in CATALOG[item_type] if item["id"] != exclude_id]
    chosen = copy.deepcopy(random.choice(options))
    return chosen

def build_design(budget=None):
    items = [
        pick_one("sofa"),
        pick_one("center_table"),
        pick_one("tv_stand"),
    ]
    total = sum(item["price"] for item in items)
    return {
        "room": ROOM,
        "layout": ["Sofa", "Center Table", "TV Stand"],
        "items": items,
        "total": total,
        "within_budget": total <= budget if budget is not None else True
    }

def with_budget(design, budget=None):
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
    design = build_design(budget)
    return jsonify(design)

@app.route("/regenerate", methods=["POST", "GET"])
def regenerate():
    budget = None
    if request.method == "POST":
        data = request.get_json() or {}
        budget = data.get("budget")
    design = build_design(budget)
    return jsonify(design)

@app.route("/regenerate-item", methods=["POST"])
def regenerate_item():
    data = request.get_json() or {}
    item_type = data.get("itemType")
    current_design = data.get("design")
    budget = data.get("budget")

    if item_type not in CATALOG:
        return jsonify({"error": "Invalid item type"}), 400

    if not current_design or "items" not in current_design:
        return jsonify({"error": "Design is required"}), 400

    updated_design = copy.deepcopy(current_design)

    for idx, item in enumerate(updated_design["items"]):
        if item["type"] == item_type:
            updated_design["items"][idx] = pick_one(item_type, exclude_id=item.get("id"))
            break

    updated_design = with_budget(updated_design, budget)
    return jsonify(updated_design)

@app.route("/update-layout", methods=["POST"])
def update_layout():
    data = request.get_json() or {}
    design = data.get("design")
    budget = data.get("budget")

    if not design or "items" not in design:
        return jsonify({"error": "Design is required"}), 400

    design = with_budget(design, budget)
    return jsonify(design)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)