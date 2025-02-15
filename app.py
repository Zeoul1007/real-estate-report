import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Houski API Configuration
API_KEY = "eff4a3de-a3a5-4deb-b025-551a6cfa7b8d"
SEARCH_URL = "https://api.houski.ca/properties"
DETAILS_URL = "https://api.houski.ca/properties/{}"

# Function to fetch property ID from address
def get_property_id(address, city, province):
    params = {
        "address": address,
        "city": city,
        "province_abbreviation": province,
        "country_abbreviation": "CA",
        "api_key": API_KEY
    }
    response = requests.get(SEARCH_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["data"]:
            return data["data"][0]["property_id"]
    return None

# Function to fetch property details using ID
def get_property_data(property_id):
    url = DETAILS_URL.format(property_id)
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    return None

@app.route("/", methods=["GET", "POST"])
def home():
    report = None

    if request.method == "POST":
        addresses_input = request.form["addresses"]
        addresses = [addr.strip() for addr in addresses_input.split(",") if addr.strip()]

        if addresses:
            properties = []
            for address in addresses:
                parts = address.split(",")
                if len(parts) < 3:
                    continue  # Skip invalid addresses

                street = parts[0].strip()
                city = parts[1].strip()
                province = parts[2].strip()

                property_id = get_property_id(street, city, province)
                if property_id:
                    property_data = get_property_data(property_id)
                    if property_data:
                        properties.append(property_data)

            if properties:
                report = generate_market_summary(properties)
            else:
                report = "No matching listings found."

    return render_template("index.html", report=report)

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    query = request.args.get("query", "")
    if not query:
        return jsonify([])

    params = {
        "query": query,
        "api_key": API_KEY
    }
    response = requests.get(SEARCH_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        suggestions = [{"address": item["address"], "city": item["city"], "province": item["province_abbreviation"]} for item in data["data"]]
        return jsonify(suggestions)

    return jsonify([])

# Function to generate market summary
def generate_market_summary(properties):
    if not properties:
        return "No market data available."

    total_price = sum(p.get("price", 0) for p in properties)
    avg_price = total_price / len(properties) if properties else 0
    avg_sqft = sum(p.get("sqft", 0) for p in properties) / len(properties) if properties else 0

    summary = f"""
    🏡 **Market Summary:**  
    There are **{len(properties)} active listings** with prices ranging from **${min(p['price'] for p in properties):,}**  
    to **${max(p['price'] for p in properties):,}**.  
    The **average price** is **${avg_price:,.2f}**, and the **average square footage** is **{avg_sqft:.0f} sq ft**.
    """

    return summary

if __name__ == "__main__":
    app.run(debug=True)








