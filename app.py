from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# =========================
# CONFIG
# =========================
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
PARTNER_TAG = os.environ.get("PARTNER_TAG")

REGION = "us-east-1"
SERVICE = "ProductAdvertisingAPI"

PAAPI_ENDPOINT = "https://webservices.amazon.com/paapi5/searchitems"


# =========================
# VALIDATE ENV VARIABLES
# =========================
def validate_env():
    if not ACCESS_KEY or not SECRET_KEY or not PARTNER_TAG:
        print("❌ Missing environment variables")
        return False
    return True


# =========================
# AMAZON API CALL (WITH DEBUG)
# =========================
def fetch_sofa_products_page(page):
    if not validate_env():
        return []

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Amz-Target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"
    }

    payload = {
        "Keywords": "sofa",
        "PartnerTag": PARTNER_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com",
        "ItemPage": page,
        "ItemCount": 10,
        "Resources": [
            "Images.Primary.Medium",
            "ItemInfo.Title",
            "Offers.Listings.Price",
            "DetailPageURL"
        ]
    }

    try:
        response = requests.post(
            PAAPI_ENDPOINT,
            json=payload,
            headers=headers
        )

        print("Amazon Status:", response.status_code)
        print("Amazon Response:", response.text)

        if response.status_code != 200:
            return []

        data = response.json()

        items = data.get("SearchResult", {}).get("Items", [])

        results = []

        for item in items:
            try:
                title = item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "")
                image = item.get("Images", {}).get("Primary", {}).get("Medium", {}).get("URL", "")

                price_info = item.get("Offers", {}).get("Listings", [])
                price = None

                if price_info:
                    price = price_info[0].get("Price", {}).get("Amount", None)

                url = item.get("DetailPageURL", "")

                if title and price:
                    results.append({
                        "name": title,
                        "price": price,
                        "image": image,
                        "link": url
                    })

            except Exception as e:
                print("Item parse error:", e)
                continue

        return results

    except Exception as e:
        print("Request error:", e)
        return []


# =========================
# FETCH MULTIPLE PAGES
# =========================
def fetch_multiple_pages(max_pages=3):
    all_products = []

    for page in range(1, max_pages + 1):
        page_results = fetch_sofa_products_page(page)
        all_products.extend(page_results)

    return all_products


# =========================
# BUDGET FILTERING
# =========================
def filter_by_budget(products, budget):
    if not budget:
        return products[:3]

    filtered = [p for p in products if p.get("price") and p["price"] <= budget]

    filtered.sort(key=lambda x: x["price"])

    return filtered[:3]


# =========================
# MOCK FALLBACK (IMPORTANT)
# =========================
def mock_products():
    return [
        {
            "name": "Demo Sofa",
            "price": 499,
            "image": "https://via.placeholder.com/150",
            "link": "https://www.amazon.com"
        },
        {
            "name": "Modern Sofa",
            "price": 799,
            "image": "https://via.placeholder.com/150",
            "link": "https://www.amazon.com"
        }
    ]


# =========================
# API ENDPOINT
# =========================
@app.route("/api/get_items", methods=["POST"])
def get_items():
    data = request.json or {}

    budget = data.get("budget")
    room = data.get("room")

    if room != "living_room":
        return jsonify({"error": "Only living room supported"}), 400

    # Fetch products
    products = fetch_multiple_pages(max_pages=3)

    # If Amazon fails → fallback to mock
    if not products:
        print("⚠️ Falling back to mock data")
        products = mock_products()

    # Filter
    filtered_products = filter_by_budget(products, budget)

    return jsonify({
        "sofa": filtered_products
    })


# =========================
# HOME ROUTE (FIX 404)
# =========================
@app.route("/")
def home():
    return "SmartFurnish backend is running 🚀"


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))