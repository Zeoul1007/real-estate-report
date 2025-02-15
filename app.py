import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Houski API Configuration
API_KEY = "eff4a3de-a3a5-4deb-b025-551a6cfa7b8d"
BASE_URL = "https://api.houski.ca/properties"

# Function to fetch property data
def get_property_data(address, city, province, country="CA"):
    headers = {"X-Api-Key": API_KEY}
    params = {
        "address": address,
        "city": city,
        "province_abbreviation": province,
        "country_abbreviation": country
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])  # Extract property list
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

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
                # Generate a formatted market summary
                report = generate_market_summary(properties)
            else:
                report = "No matching listings found."

    return render_template("index.html", report=report)

# Function to generate a market summary
def generate_market_summary(listings):
    if not listings:
        return "No market data available."

    summary = "📊 **Market Summary:**\n\n"
    for listing in listings:
        summary += f"🏡 **{listing.get('address', 'Unknown Address')}**\n"
        summary += f"- **Property ID:** {listing.get('property_id', 'N/A')}\n\n"

    return summary

if __name__ == "__main__":
    app.run(debug=True)

