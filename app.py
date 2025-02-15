import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Houski API Configuration
API_KEY = "eff4a3de-a3a5-4deb-b025-551a6cfa7b8d"
BASE_URL = "https://api.houski.ca/properties"

# Function to fetch property data from Houski API
def get_property_data(addresses):
    headers = {"X-Api-Key": API_KEY}
    listings = []

    for address in addresses:
        params = {
            "address": address,
            "country_abbreviation": "CA",  # Canada
            "results_per_page": "1"
        }
        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                listings.append(data["data"][0])  # Get first result
        else:
            print(f"Error fetching data for {address}: {response.status_code}")

    return listings

@app.route("/", methods=["GET", "POST"])
def home():
    report = None

    if request.method == "POST":
        address_input = request.form["addresses"]
        addresses = [addr.strip() for addr in address_input.split(",") if addr.strip()]

        if addresses:
            properties = get_property_data(addresses)

            if properties:
                report = generate_market_summary(properties)
            else:
                report = "No matching listings found."

    return render_template("index.html", report=report)

# Function to generate a market summary
def generate_market_summary(listings):
    if not listings:
        return "No market data available."

    total_price = sum(listing.get("price", 0) for listing in listings if listing.get("price"))
    avg_price = total_price / len(listings) if total_price else 0
    avg_sqft = sum(listing.get("sqft", 0) for listing in listings if listing.get("sqft")) / len(listings) if total_price else 0

    summary = f"""
    🏡 **Market Summary:**  
    Found **{len(listings)} properties**.  
    Price Range: **${min(l['price'] for l in listings if l.get('price')):,} - ${max(l['price'] for l in listings if l.get('price')):,}**  
    **Average Price**: ${avg_price:,.2f}  
    **Average Size**: {avg_sqft:.0f} sq ft  
    """

    return summary

# API Route for Autocomplete Search (For Frontend)
@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query")
    if not query:
        return jsonify([])

    headers = {"X-Api-Key": API_KEY}
    params = {"address": query, "country_abbreviation": "CA", "results_per_page": "5"}
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        results = [{"address": item["address"]} for item in data.get("data", [])]
        return jsonify(results)
    
    return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)








