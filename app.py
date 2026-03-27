from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import json
import hashlib
import hmac
import datetime

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
ENDPOINT = "https://webservices.amazon.com/paapi5/searchitems"
HOST = "webservices.amazon.com"


# =========================
# SIGV4 HELPERS
# =========================
def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = hmac.new(k_date, region_name.encode("utf-8"), hashlib.sha256).digest()
    k_service = hmac.new(k_region, service_name.encode("utf-8"), hashlib.sha256).digest()
    k_signing = hmac.new(k_service, b"aws4_request", hashlib.sha256).digest()
    return k_signing


# =========================
# AMAZON API CALL (SIGNED)
# =========================
def fetch_sofa_products_page(page):
    method = "POST"
    canonical_uri = "/paapi5/searchitems"
    canonical_querystring = ""

    t = datetime.datetime.utcnow()
    amz_date = t.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = t.strftime("%Y%m%d")

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

    payload_json = json.dumps(payload)

    # Canonical headers
    canonical_headers = (
        f"content-encoding:amz-1.0\n"
        f"host:{HOST}\n"
        f"x-amz-date:{amz_date}\n"
        f"x-amz-target:com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems\n"
    )

    signed_headers = "content-encoding;host;x-amz-date;x-amz-target"

    payload_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()

    canonical_request = "\n".join([
        method,
        canonical_uri,
        canonical_querystring,
        canonical_headers,
        signed_headers,
        payload_hash
    ])

    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{REGION}/{SERVICE}/aws4_request"

    string_to_sign = "\n".join([
        algorithm,
        amz_date,
        credential_scope,
        hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    ])

    signing_key = get_signature_key(SECRET_KEY, date_stamp, REGION, SERVICE)

    signature = hmac.new(
        signing_key,
        string_to_sign.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    authorization_header = (
        f"{algorithm} "
        f"Credential={ACCESS_KEY}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )

    headers = {
        "Content-Encoding": "amz-1.0",
        "Content-Type": "application/json; charset=utf-8",
        "X-Amz-Date": amz_date,
        "X-Amz-Target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems",
        "Authorization": authorization_header
    }

    response = requests.post(ENDPOINT, data=payload_json, headers=headers)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    if response.status_code != 200:
        return []

    data = response.json()

    items = data.get("SearchResult", {}).get("Items", [])

    results = []

    for item in items:
        try:
            title = item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "")
            image = item.get("Images", {}).get("Primary", {}).get("Medium", {}).get("URL", "")

            price = None
            listings = item.get("Offers", {}).get("Listings", [])
            if listings:
                price = listings[0].get("Price", {}).get("Amount", None)

            url = item.get("DetailPageURL", "")

            if title and price:
                results.append({
                    "name": title,
                    "price": price,
                    "image": image,
                    "link": url
                })

        except Exception as e:
            print("Parse error:", e)

    return results


# =========================
# MULTI PAGE FETCH
# =========================
def fetch_multiple_pages(max_pages=3):
    all_products = []

    for page in range(1, max_pages + 1):
        products = fetch_sofa_products_page(page)
        all_products.extend(products)

    return all_products


# =========================
# BUDGET FILTER
# =========================
def filter_by_budget(products, budget):
    filtered = [p for p in products if p["price"] and p["price"] <= budget]
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

    products = fetch_multiple_pages(max_pages=3)
    filtered = filter_by_budget(products, budget)

    return jsonify({
        "sofa": filtered
    })


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))