import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Houski API Configuration
API_KEY = "eff4a3de-a3a5-4deb-b025-551a6cfa7b8d"
BASE_URL = "https://api.houski.ca/properties"

# Function to fetch property data
def get_property_data(address, city, province, country="CA"):
    headers = {"X-Api-Key": API_KEY}
    
    # Auto-format input to match API requirements
    formatted_address = address.strip().replace(" ", "-").lower()
    formatted_city = city.strip().replace(" ", "-").lower()
    formatted_province = province.strip().upper()

    params = {
        "address": formatted_address,
        "city": formatted_city,
        "province_abbreviation": formatted_province,
        "country_abbreviation": country.upper(),
        "results_per_page": 3,  # Get up to 3 results per request
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])  # Extract property list
    elif response.status_code == 400:
        return f"⚠️ Bad request: {response.json().get('error', 'Unknown error')}"
    else:
        return f"❌ API Error {response.status_code}: {response.text}"

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    example_format = "Example: 5 Thistledown Drive, Brantford, ON"

    if request.method == "POST":
        address_input = request.form.get("address", "").strip()
        city_input = request.form.get("city", "").strip()
        province_input = request.form.get("province", "").strip()

        if not address_input or not city_input or not province_input:
            report = "⚠️ Please enter a valid address, city, and province."
        else:
            properties = get_property_data(address_input, city_input, province_input)

            if isinstance(properties, str):  # API error returned as a string
                report = properties
            elif properties:
                report = generate_market_summary(properties)
            else:
                report = "⚠️ No matching listings found. Please check the format."

    return render_template("index.html", report=report, example_format=example_format)

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




