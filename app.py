import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# RentCast API Configuration
API_KEY = "78fae72b7ea847b986ca17df34c8fc76"
BASE_URL = "https://api.rentcast.io/v1/properties"

# Function to fetch property data
def get_property_data(mls_ids):
    headers = {"X-Api-Key": API_KEY}
    listings = []

    for mls_id in mls_ids:
        params = {"mlsId": mls_id}  # Use MLS ID as query parameter
        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data:
                listings.append(data)
        else:
            print(f"Failed to fetch MLS ID {mls_id}: {response.status_code}")

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
                # Generate a formatted market summary
                report = generate_market_summary(properties)
            else:
                report = "No matching listings found."

    return render_template("index.html", report=report)

# Function to generate a market summary
def generate_market_summary(listings):
    if not listings:
        return "No market data available."

    total_price = sum(listing.get("price", 0) for listing in listings)
    avg_price = total_price / len(listings) if listings else 0
    avg_sqft = sum(listing.get("sqft", 0) for listing in listings) / len(listings) if listings else 0

    summary = f"""
    🏡 **Market Summary:**  
    There are **{len(listings)} active listings** with prices ranging from **${min(l['price'] for l in listings):,}**  
    to **${max(l['price'] for l in listings):,}**.  
    The **average price** is **${avg_price:,.2f}**, and the **average square footage** is **{avg_sqft:.0f} sq ft**.
    """

    return summary

if __name__ == "__main__":
    app.run(debug=True)
