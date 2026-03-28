from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

# Mock design data (focused on Sofa, Center Table, TV Stand)
designs = [
    {
        "layout": ["Sofa", "Center Table", "TV Stand"],
        "items": [
            {"name": "Modern 3-Seater Sofa", "price": 700},
            {"name": "Wood Center Table", "price": 250},
            {"name": "Minimal TV Stand", "price": 300},
        ],
    },
    {
        "layout": ["Sofa", "TV Stand", "Center Table"],
        "items": [
            {"name": "L-Shaped Sofa", "price": 900},
            {"name": "Glass Center Table", "price": 300},
            {"name": "Floating TV Stand", "price": 350},
        ],
    },
    {
        "layout": ["TV Stand", "Sofa", "Center Table"],
        "items": [
            {"name": "Fabric Sofa Set", "price": 650},
            {"name": "Marble Center Table", "price": 400},
            {"name": "Classic TV Cabinet", "price": 500},
        ],
    },
]

def build_design(design, budget=None):
    total = sum(item["price"] for item in design["items"])
    return {
        "layout": design["layout"],
        "items": design["items"],
        "total": total,
        "within_budget": total <= budget if budget else True
    }

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()

    budget = data.get("budget")
    style = data.get("style")
    room = data.get("room")

    design = random.choice(designs)
    response = build_design(design, budget)

    return jsonify(response)

@app.route("/regenerate", methods=["GET"])
def regenerate():
    design = random.choice(designs)
    response = build_design(design)

    return jsonify(response)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SmartFurnish Backend Running"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)