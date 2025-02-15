import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Houski API Configuration
API_KEY = "eff4a3de-a3a5-4deb-b025-551a6cfa7b8d"
BASE_URL = "https://api.houski.ca/properties"

# Function to fetch property data
def get_property_data(address, city, province):
    params = {
        "address": address,
        "city": city,
        "province_abbreviation": province,
        "country_abbreviation": "CA",
        "api_key": API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            return data["data"]
    
    return None

@app.route("/", methods=["GET", "POST"])
def home():
    report = None

    if request.method == "POST":
        address_input = request.form["address"]
        city_input = request.form["city"]
        province_input = request.form["province"]

        if address_input and city_input and province_input:
            properties = get_property_data(address_input, city_input, province_input)

            if properties:
                report = generate_market_summary(properties)
            else:
                report = "No matching listings found."

    return render_template("index.html", report=report)

# Function to generate a market summary
def generate_market_summary(listings):
    if not listings:
        return "No market data available."

    report_lines = ["📊 **Market Summary:**"]

    for listing in listings:
        address = listing.get("address", "Unknown Address")
        price = listing.get("price", "N/A")
        bedrooms = listing.get("bedroom", "N/A")
        bathrooms = listing.get("bathroom_full", "N/A")

        report_lines.append(
            f"- **{address}**\n"
            f"  - 💰 **Price:** {price if price != 'N/A' else 'Not Available'}\n"
            f"  - 🛏 **Bedrooms:** {bedrooms}\n"
            f"  - 🛁 **Bathrooms:** {bathrooms}\n"
        )

    return "\n".join(report_lines)

if __name__ == "__main__":
    app.run(debug=True)





