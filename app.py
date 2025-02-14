import requests
import json
import os
from flask import Flask, request, render_template

app = Flask(__name__)

# RealtyMole API Key (Stored in Railway Environment Variables)
API_KEY = os.getenv("REALTYMOLE_API_KEY", "78fae72b7ea847b986ca17df34c8fc76")
BASE_URL = "https://api.realtymole.com/v1/properties"

def get_property_data(mls_ids):
    """ Fetch property data from RealtyMole API based on MLS listing IDs. """
    property_listings = []
    
    for mls_id in mls_ids:
        params = {
            "apiKey": API_KEY,
            "listingId": mls_id
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data:
                property_listings.append(data)
    
    return property_listings

def generate_market_summary(properties):
    """ Generate a market summary based on retrieved listings. """
    if not properties:
        return "No matching listings found."

    prices = [p.get("price", 0) for p in properties]
    sq_ft = [p.get("squareFootage", 0) for p in properties]
    days_on_market = [p.get("daysOnMarket", 0) for p in properties]

    avg_price = sum(prices) / len(prices) if prices else 0
    avg_sq_ft = sum(sq_ft) / len(sq_ft) if sq_ft else 0
    avg_days = sum(days_on_market) / len(days_on_market) if days_on_market else 0

    summary = (
        f"There are {len(properties)} active listings with prices ranging from "
        f"${min(prices):,.0f} to ${max(prices):,.0f}. "
        f"The average price is ${avg_price:,.2f}, "
        f"with an average square footage of {avg_sq_ft:.0f} sq ft. "
        f"Properties have been on the market for an average of {avg_days:.0f} days."
    )

    return summary

@app.route("/", methods=["GET", "POST"])
def home():
    """ Main page for entering MLS listing IDs and generating reports. """
    report = ""
    if request.method == "POST":
        mls_ids = request.form.get("mls_ids")
        if mls_ids:
            mls_ids = [id.strip() for id in mls_ids.split(",")]
            properties = get_property_data(mls_ids)
            report = generate_market_summary(properties)
    
    return render_template("index.html", report=report)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)






