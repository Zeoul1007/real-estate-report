import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# ✅ Correct MLS API URL & Authentication Key
MLS_API_URL = "https://real-estate-api.example.com/listings"  # 🔹 This is the correct API URL
MLS_API_KEY = "YOUR_ACTUAL_API_KEY_HERE"  # 🔹 Replace with the working API key

def fetch_mls_data(listing_ids):
    """
    Fetch MLS data for given listing IDs from the API.
    """
    headers = {"Authorization": f"Bearer {MLS_API_KEY}"}
    params = {"ids": ",".join(listing_ids)}

    try:
        response = requests.get(MLS_API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data or "listings" not in data:
            print("⚠️ No listings found in API response.")
            return []
        
        return data["listings"]

    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return []

def generate_market_summary(listings):
    """
    Generate a narrative market summary from active & sold listings.
    """
    if not listings:
        return "No matching listings found."

    active_listings = [listing for listing in listings if listing["status"] == "Active"]
    sold_listings = [listing for listing in listings if listing["status"] in ["Sold", "Closed"]]

    if not active_listings and not sold_listings:
        return "No active or sold listings found."

    # Extract pricing & market trends
    active_prices = [listing["price"] for listing in active_listings]
    sold_prices = [listing["price"] for listing in sold_listings]
    active_sqft = [listing["sqft"] for listing in active_listings if "sqft" in listing]
    days_on_market = [listing["days_on_market"] for listing in listings if "days_on_market" in listing]

    summary = "**📊 Market Summary:**\n"

    if active_listings:
        summary += (
            f"🏠 There are **{len(active_listings)} active listings** "
            f"ranging from **${min(active_prices):,}** to **${max(active_prices):,}**.\n"
            f"The **average price** is **${sum(active_prices)/len(active_prices):,.2f}** "
            f"and the **average square footage** is **{sum(active_sqft)/len(active_sqft):.0f} sq ft**.\n"
        )

    if sold_listings:
        summary += (
            f"✅ There are **{len(sold_listings)} sold listings** "
            f"with sale prices ranging from **${min(sold_prices):,}** to **${max(sold_prices):,}**.\n"
        )

    if days_on_market:
        summary += (
            f"⏳ The average time on market is **{sum(days_on_market)/len(days_on_market):.1f} days**.\n"
        )

    return summary

@app.route("/", methods=["GET", "POST"])
def home():
    """
    Home page with MLS listing search and market analysis.
    """
    report = ""
    if request.method == "POST":
        listing_ids = request.form["mls_ids"].split(",")
        listing_ids = [id.strip() for id in listing_ids if id.strip()]  # Remove empty entries

        if listing_ids:
            listings = fetch_mls_data(listing_ids)
            market_summary = generate_market_summary(listings)

            # Render listing details & market summary
            report = "\n\n".join(
                [
                    f"🏡 **MLS ID:** {listing['id']}\n"
                    f"📍 **Address:** {listing['address']}\n"
                    f"💰 **Price:** ${listing['price']:,}\n"
                    f"🛏️ **Beds:** {listing['beds']}  |  🛁 **Baths:** {listing['baths']}\n"
                    f"📏 **Square Footage:** {listing.get('sqft', 'N/A')} sqft\n"
                    f"📊 **Status:** {listing['status']}"
                    for listing in listings
                ]
            )

            report += f"\n\n{market_summary}"

    return render_template("index.html", report=report)

if __name__ == "__main__":
    app.run(debug=True)





