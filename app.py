from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Simulated listing data for Ontario, Canada
def get_listing_data(mls_ids):
    listings = {
        "40687604": {"address": "123 Main St, Toronto, ON", "beds": 3, "baths": 2, "price": 550000, "status": "Active", "sqft": 1500, "days_on_market": 30},
        "40692301": {"address": "456 Oak Ave, Ottawa, ON", "beds": 4, "baths": 3, "price": 720000, "status": "Active", "sqft": 2000, "days_on_market": 45},
        "40659114": {"address": "789 Maple Rd, Mississauga, ON", "beds": 2, "baths": 1, "price": 430000, "status": "Sold", "sqft": 1200, "days_on_market": 20},
    }
    
    return {mls_id: listings.get(mls_id, None) for mls_id in mls_ids}

@app.route("/", methods=["GET", "POST"])
def home():
    report = None

    if request.method == "POST":
        mls_input = request.form.get("mls_ids", "")
        mls_ids = [mls.strip() for mls in mls_input.split(",") if mls.strip()]
        
        listing_data = get_listing_data(mls_ids)

        active_listings = [listing for listing in listing_data.values() if listing and listing["status"] == "Active"]
        sold_listings = [listing for listing in listing_data.values() if listing and listing["status"] == "Sold"]

        report = "🏡 **Real Estate Report**\n\n"

        # Show Listing Details First
        for mls_id, listing in listing_data.items():
            if listing:
                report += f"📌 **MLS ID: {mls_id}**\n"
                report += f"🏠 **{listing['address']}**\n"
                report += f"🛏 {listing['beds']} beds | 🛁 {listing['baths']} baths\n"
                report += f"💰 **Price:** ${listing['price']:,}\n"
                report += f"📌 **Status:** {listing['status']}\n"
                report += "----------------------------------------\n"

        # Market Summary at the End
        if active_listings:
            active_prices = [listing["price"] for listing in active_listings]
            active_sqft = [listing["sqft"] for listing in active_listings]
            active_days = [listing["days_on_market"] for listing in active_listings]

            report += "\n📊 **Market Summary:**\n"
            report += f"There are **{len(active_listings)} active listings** with prices ranging from **${min(active_prices):,}** to **${max(active_prices):,}**.\n"
            report += f"The **average price** is **${sum(active_prices) / len(active_prices):,.2f}**, and the **average square footage** is **{sum(active_sqft) / len(active_sqft):.0f} sq ft**.\n"
            report += f"The **average days on market** is **{sum(active_days) / len(active_days):.0f} days**.\n"

        if sold_listings:
            sold_prices = [listing["price"] for listing in sold_listings]
            sold_days = [listing["days_on_market"] for listing in sold_listings]

            report += "\n**Sold Listings:**\n"
            report += f"- **{len(sold_listings)} closed listings** with sale prices ranging from **${min(sold_prices):,}** to **${max(sold_prices):,}**.\n"
            report += f"- Fastest sale completed in **{min(sold_days)} days**, longest sale took **{max(sold_days)} days**.\n"

    return render_template("index.html", report=report)

if __name__ == "__main__":
    app.run(debug=True)

