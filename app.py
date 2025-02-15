import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Houski API Configuration
API_KEY = "eff4a3de-a3a5-4deb-b025-551a6cfa7b8d"
BASE_URL = "https://api.houski.ca/properties"

# Function to fetch property data
def get_property_data(addresses):
    headers = {"X-Api-Key": API_KEY}
    listings = []

    for address in addresses:
        params = {
            "address": address,
            "country_abbreviation": "CA",
            "results_per_page": "1",
        }
        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                listings.append(data["data"][0])  # Extract first result
        else:
            print(f"Failed to fetch data for {address}: {response.status_code}")

    return listings

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    selected_addresses = []

    if request.method == "POST":
        address_input = request.form["addresses"]
        selected_addresses = [addr.strip() for addr in address_input.split(",") if addr.strip()]

        if selected_addresses:
            properties = get_property_data(selected_addresses)
            report = generate_market_summary(properties) if properties else "No matching listings found."

    return render_template("index.html", report=report, selected_addresses=selected_addresses)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query")
    if not query:
        return jsonify([])

    headers = {"X-Api-Key": API_KEY}
    params = {"query": query, "results_per_page": 5}
    response = requests.get(f"{BASE_URL}/search", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        suggestions = [result["address"] for result in data.get("data", [])]
        return jsonify(suggestions)

    return jsonify([])

# Function to generate a market summary
def generate_market_summary(listings):
    if not listings:
        return "No market data available."

    total_price = sum(listing.get("price", 0) for listing in listings)
    avg_price = total_price / len(listings) if listings else 0
    avg_sqft = sum(listing.get("sqft", 0) for listing in listings) / len(listings) if listings else 0

    summary = f"""
    <img src='/static/logo.png' alt='Pay It Forward Realty' width='200'><br>
    🏡 **Market Summary:**  
    There are **{len(listings)} active listings** with prices ranging from **${min(l['price'] for l in listings):,}**  
    to **${max(l['price'] for l in listings):,}**.  
    The **average price** is **${avg_price:,.2f}**, and the **average square footage** is **{avg_sqft:.0f} sq ft**.
    """

    return summary

if __name__ == "__main__":
    app.run(debug=True)






