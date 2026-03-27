from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from requests_aws4auth import AWS4Auth

app = Flask(__name__)
CORS(app)

# =========================
# CONFIG (ADD YOUR KEYS)
# =========================
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
PARTNER_TAG = os.environ.get("PARTNER_TAG")

REGION = "us-east-1"
SERVICE = "ProductAdvertisingAPI"

PAAPI_ENDPOINT = "https://webservices.amazon.com/paapi5/searchitems"


# =========================
# AMAZON API CALL (ONE PAGE)
# =========================
def fetch_sofa_products_page(page):
    auth = AWS4Auth(
        ACCESS_KEY,
        SECRET_KEY,
        REGION,
        SERVICE
    )

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

    response = requests.post(
        PAAPI_ENDPOINT,
        auth=auth,
        json=payload,
        headers=headers
    )

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

            results.append({
                "name": title,
                "price": price,
                "image": image,
                "link": url
            })

        except Exception:
            continue

    return results


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
    filtered = []

    for product in products:
        if product["price"] and product["price"] <= budget:
            filtered.append(product)

    # Optional: sort by price ascending (best fit)
    filtered.sort(key=lambda x: x["price"])

    return filtered[:3]


# =========================
# API ENDPOINT
# =========================
@app.route("/api/get_items", methods=["POST"])
def get_items():
    data = request.json

    budget = data.get("budget")
    room = data.get("room")

    if room != "living_room":
        return jsonify({"error": "Only living room supported"}), 400

    # Step 1: Fetch multiple pages
    products = fetch_multiple_pages(max_pages=3)

    # Step 2: Filter by budget
    filtered_products = filter_by_budget(products, budget)

    return jsonify({
        "sofa": filtered_products
    })


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))