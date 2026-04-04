from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os
import copy
from urllib.parse import urljoin

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
            "front": {"x": 120, "y": 285, "width": 300, "height": 145},
            "left": {"x": 150, "y": 290, "width": 250, "height": 138},
            "right": {"x": 520, "y": 290, "width": 250, "height": 138},
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
            "front": {"x": 105, "y": 275, "width": 330, "height": 155},
            "left": {"x": 140, "y": 280, "width": 275, "height": 145},
            "right": {"x": 495, "y": 280, "width": 275, "height": 145},
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
            "front": {"x": 135, "y": 295, "width": 255, "height": 128},
            "left": {"x": 165, "y": 298, "width": 220, "height": 122},
            "right": {"x": 545, "y": 298, "width": 220, "height": 122},
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
            "front": {"x": 425, "y": 325, "width": 145, "height": 88},
            "left": {"x": 430, "y": 328, "width": 130, "height": 82},
            "right": {"x": 360, "y": 328, "width": 130, "height": 82},
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
            "front": {"x": 430, "y": 326, "width": 142, "height": 84},
            "left": {"x": 432, "y": 330, "width": 126, "height": 80},
            "right": {"x": 362, "y": 330, "width": 126, "height": 80},
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
            "front": {"x": 420, "y": 322, "width": 158, "height": 92},
            "left": {"x": 425, "y": 326, "width": 140, "height": 86},
            "right": {"x": 355, "y": 326, "width": 140, "height": 86},
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
            "front": {"x": 640, "y": 190, "width": 195, "height": 92},
            "left": {"x": 650, "y": 198, "width": 165, "height": 82},
            "right": {"x": 105, "y": 198, "width": 165, "height": 82},
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
            "front": {"x": 645, "y": 192, "width": 192, "height": 86},
            "left": {"x": 653, "y": 200, "width": 160, "height": 78},
            "right": {"x": 108, "y": 200, "width": 160, "height": 78},
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
            "front": {"x": 635, "y": 188, "width": 202, "height": 96},
            "left": {"x": 648, "y": 196, "width": 168, "height": 84},
            "right": {"x": 102, "y": 196, "width": 168, "height": 84},
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

REALVIEW_BACKGROUNDS = {
    "front": "/assets/rooms/livingroom/front.jpg",
    "left": "/assets/rooms/livingroom/left.jpg",
    "right": "/assets/rooms/livingroom/right.jpg",
}

FALLBACK_REAL_IMAGE = "/static/assets/generated/front-natural-room.jpg"


def pick_one(item_type, exclude_id=None):
    options = [item for item in CATALOG[item_type] if item["id"] != exclude_id]
    return copy.deepcopy(random.choice(options))


def serialize_item_for_angle(item, angle):
    return {
        "id": item.get("id"),
        "type": item.get("type"),
        "name": item.get("name"),
        "price": item.get("price"),
        "image": item.get("images", {}).get(angle) or item.get("images", {}).get("front"),
        "position": copy.deepcopy(item.get("positions", {}).get(angle, {})),
        "brand": item.get("brand"),
        "color": item.get("color"),
        "material": item.get("material"),
        "in_stock": item.get("in_stock"),
        "dimensions": item.get("dimensions"),
        "rating": item.get("rating"),
        "reviews": item.get("reviews"),
        "purchases": item.get("purchases"),
    }


def build_realview(design):
    items = design.get("items", [])
    views = {}

    for angle in ROOM["angles"]:
        angle_items = []

        for item in items:
            position = item.get("positions", {}).get(angle)
            if position:
                angle_items.append(serialize_item_for_angle(item, angle))

        views[angle] = {
            "angle": angle,
            "background": REALVIEW_BACKGROUNDS.get(angle),
            "room": {
                "width": ROOM["width"],
                "height": ROOM["height"]
            },
            "items": angle_items
        }

    return {
        "defaultAngle": "front",
        "angles": ROOM["angles"],
        "views": views
    }


def build_design(budget=None, include_realview=True):
    items = [
        pick_one("sofa"),
        pick_one("center_table"),
        pick_one("tv_stand"),
    ]
    total = sum(item["price"] for item in items)

    design = {
        "room": ROOM,
        "items": items,
        "total": total,
        "within_budget": total <= budget if budget is not None else True
    }

    if include_realview:
        design["realview"] = build_realview(design)

    return design


def refresh_totals(design, budget=None, include_realview=True):
    total = sum(item["price"] for item in design["items"])
    design["total"] = total
    design["within_budget"] = total <= budget if budget is not None else True

    if include_realview:
        design["realview"] = build_realview(design)

    return design


def get_public_base_url():
    return os.environ.get("PUBLIC_BASE_URL", "https://smartfurnish-backend.onrender.com").rstrip("/")


def absolute_public_url(path):
    if not path:
        return ""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{get_public_base_url()}{path}"


def build_real_image_prompt(payload):
    scene = payload.get("scene", {})
    sofa = scene.get("sofa", {})
    table = scene.get("table", {})
    room_type = payload.get("roomType", "living_room")
    view = payload.get("view", "front")

    sofa_name = sofa.get("name", "curved sofa")
    sofa_material = sofa.get("material", "soft fabric")
    sofa_color = sofa.get("color", "off-white")
    sofa_style = sofa.get("style", "modern")

    table_name = table.get("name", "round coffee table")
    table_material = table.get("material", "wood")
    table_color = table.get("color", "beige")
    table_style = table.get("style", "minimal")

    prompt = f"""
Photorealistic {view} view of a {room_type.replace('_', ' ')}.
A natural elegant living room with a {sofa_color.lower()} {sofa_style.lower()} {sofa_name.lower()} made of {sofa_material.lower()} as the main focal point.
In front of it, a {table_color.lower()} {table_style.lower()} {table_name.lower()} made of {table_material.lower()}.
The furniture should feel naturally placed in a real room, with correct scale, realistic shadows, soft daylight, light wood flooring, a subtle neutral rug, clean off-white wall, tasteful minimal decor, premium apartment interior styling, warm ambient light, and camera composition from the front view.
Do not show floating furniture. Make the room look like a genuine interior photograph.
""".strip()

    return " ".join(prompt.split())

def generate_real_image(payload):
    """
    Phase 1 implementation:
    - Build a strong prompt from the finalized 3D scene
    - Return a fallback realistic image so the feature works end-to-end now

    Phase 2:
    - Replace this with a call to your image generation provider
    - Return the provider image URL or a saved generated asset URL
    """
    prompt = build_real_image_prompt(payload)

    # Replace this later with real model output.
    # For now, make sure this image exists in your frontend/public or backend-served static assets path.
    image_url = absolute_public_url(FALLBACK_REAL_IMAGE)

    return {
        "imageUrl": image_url,
        "promptUsed": prompt,
        "generationMode": "fallback_image"
    }


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "SmartFurnish Backend Running"})


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() or {}
    budget = data.get("budget")
    include_realview = data.get("includeRealview", True)
    return jsonify(build_design(budget, include_realview=include_realview))


@app.route("/generate-realview", methods=["POST"])
def generate_realview():
    data = request.get_json() or {}
    design = copy.deepcopy(data.get("design"))

    if not design or "items" not in design:
        return jsonify({"error": "Invalid request"}), 400

    return jsonify({
        "realview": build_realview(design)
    })


@app.route("/generate-real-image", methods=["POST"])
def generate_real_image_route():
    payload = request.get_json(silent=True) or {}

    if "scene" not in payload:
        return jsonify({"error": "Missing scene in request payload"}), 400

    try:
        result = generate_real_image(payload)
        return jsonify({
            "success": True,
            "imageUrl": result["imageUrl"],
            "promptUsed": result["promptUsed"],
            "generationMode": result["generationMode"],
        })
    except Exception as exc:
        return jsonify({"error": f"Failed to generate real image: {str(exc)}"}), 500


@app.route("/regenerate", methods=["POST"])
def regenerate():
    data = request.get_json() or {}
    budget = data.get("budget")
    include_realview = data.get("includeRealview", True)
    return jsonify(build_design(budget, include_realview=include_realview))


@app.route("/regenerate-item", methods=["POST"])
def regenerate_item():
    data = request.get_json() or {}
    item_type = data.get("itemType")
    design = copy.deepcopy(data.get("design"))
    budget = data.get("budget")
    include_realview = data.get("includeRealview", True)

    if not design or item_type not in CATALOG:
        return jsonify({"error": "Invalid request"}), 400

    for i, item in enumerate(design["items"]):
        if item["type"] == item_type:
            design["items"][i] = pick_one(item_type, exclude_id=item["id"])
            break

    return jsonify(refresh_totals(design, budget, include_realview=include_realview))


@app.route("/remove-item", methods=["POST"])
def remove_item():
    data = request.get_json() or {}
    item_type = data.get("itemType")
    design = copy.deepcopy(data.get("design"))
    budget = data.get("budget")
    include_realview = data.get("includeRealview", True)

    if not design:
        return jsonify({"error": "Invalid request"}), 400

    design["items"] = [item for item in design["items"] if item["type"] != item_type]
    return jsonify(refresh_totals(design, budget, include_realview=include_realview))


@app.route("/update-layout", methods=["POST"])
def update_layout():
    data = request.get_json() or {}
    design = copy.deepcopy(data.get("design"))
    budget = data.get("budget")
    include_realview = data.get("includeRealview", True)

    if not design:
        return jsonify({"error": "Invalid request"}), 400

    return jsonify(refresh_totals(design, budget, include_realview=include_realview))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)