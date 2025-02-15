import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Houski API Configuration
API_KEY = "eff4a3de-a3a5-4deb-b025-551a6cfa7b8d"
BASE_URL = "https://api.houski.ca/v1/properties"

# Function to fetch property data from Houski API
def get_property_data(mls_ids):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    listings = []

    for mls_id in mls_ids:
        params = {"listingId": mls_id}  # Houski API expects "listingId"
        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                if data and "properties" in data:
                    listings.extend(data["properties"])
                else:
                    print(f"No data found for MLS ID {mls_id}. Response: {data}")
            except requests.exceptions.JSONDecodeError:
                print(f"Error decoding JSON for MLS ID {mls_id}. Response text: {response.text}")
        else:
            print(f"Failed to fetch MLS ID {mls_id}: {response.status_code} - {response.text}")

    return listings

@app.route("/", methods=["GET", "POST"])
def home():
    report = None

    if request.method == "POST":
        mls_input = request.form["mls_ids"]
        mls_ids = [id.strip() for id in mls_input.split(",") if id.strip()]

        if mls_ids:
            properties = get_property_data(mls_ids)

            if properties:
                report = generate_market_summary(properties)
            else:
                report = "No matching listings found."

    return render_template("index.html", report=report)

# Function to generate a market summary
def generate_market_summary(listings):
    if not listings:
        return "No market data available."

    total_price = sum(l.get("price", 0) for l in listings if "price" in l)
    avg_price = total_price / len(listings) if listings else 0
    avg_sqft = sum(l.get("sqft", 0) for l in listings if "sqft" in l) / len(listings) if listings else 0
    min_price = min((l.get("price", 0) for l in listings if "price" in l), default=0)
    max_price = max((l.get("price", 0) for l in listings if "price" in l), default=0)

    summary = f"""
    🏡 **Market Summary:**  
    There are **{len(listings)} active listings** with prices ranging from **${min_price:,.2f}**  
    to **${max_price:,.2f}**.  
    The **average price** is **${avg_price:,.2f}**, and the **average square footage** is **{avg_sqft:.0f} sq ft**.
    """

    return summary

if __name__ == "__main__":
    app.run(debug=True)
