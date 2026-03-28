from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =========================
# CLEAN DATASET (REAL IMAGES)
# =========================

SOFA_DATA = [
    {
        "name": "Modern Grey Sofa",
        "price": 799,
        "image": "https://images.unsplash.com/photo-1586023492125-27b2c045efd7",
        "link": "https://www.amazon.com"
    },
    {
        "name": "Luxury Fabric Sofa",
        "price": 999,
        "image": "https://images.unsplash.com/photo-1616628182507-2a1f9e5c5e3b",
        "link": "https://www.amazon.com"
    },
    {
        "name": "Compact Sofa",
        "price": 499,
        "image": "https://images.unsplash.com/photo-1598300053653-4f0a98c1c2c7",
        "link": "https://www.amazon.com"
    }
]

COFFEE_TABLE_DATA = [
    {
        "name": "Wood Coffee Table",
        "price": 199,
        "image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
        "link": "https://www.amazon.com"
    },
    {
        "name": "Glass Coffee Table",
        "price": 249,
        "image": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91",
        "link": "https://www.amazon.com"
    },
    {
        "name": "Minimal Table",
        "price": 149,
        "image": "https://images.unsplash.com/photo-1567016432779-094069958ea5",
        "link": "https://www.amazon.com"
    }
]

TV_STAND_DATA = [
    {
        "name": "Modern TV Stand",
        "price": 299,
        "image": "https://images.unsplash.com/photo-1615874959474-d609969a20ed",
        "link": "https://www.amazon.com"
    },
    {
        "name": "Wood TV Console",
        "price": 349,
        "image": "https://images.unsplash.com/photo-1600585154783-9c7c0f6d7c1f",
        "link": "https://www.amazon.com"
    },
    {
        "name": "Minimal TV Unit",
        "price": 199,
        "image": "https://images.unsplash.com/photo-1595526114035-0d45ed16cfbf",
        "link": "https://www.amazon.com"
    }
]

# =========================
# FILTER BY BUDGET
# =========================
def filter_items(data, budget):
    return sorted(
        [item for item in data if item["price"] <= budget],
        key=lambda x: x["price"]
    )[:3]


# =========================
# API
# =========================
@app.route("/api/get_items", methods=["POST"])
def get_items():
    data = request.json
    budget = data.get("budget", 1000)

    return jsonify({
        "sofa": filter_items(SOFA_DATA, budget),
        "coffee_table": filter_items(COFFEE_TABLE_DATA, budget),
        "tv_stand": filter_items(TV_STAND_DATA, budget)
    })


# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)