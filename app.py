from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# MLS API Details (Update with correct endpoint & API key)
MLS_API_URL = "https://example.com/mls-api"  # Replace with the correct API URL
API_KEY = "your_api_key_here"  # Replace with your actual API key

def fetch_mls_data(mls_ids):
    """Fetch real estate listings from the MLS API."""
    listings = []
    headers = {"Authorization": f"Bearer {API_KEY}"}

    for mls_id in mls_ids:
        response = requests.get(f"{MLS_API_URL}/{mls_id}", headers=headers)

        if response.status_code == 200:
            data = response.json()
            listings.append({
                "MLS ID": data.get("mls_id"),
                "Address": data.get("address"),
                "Beds": data.get("beds"),
                "Baths": data.get("baths"),
                "Price": data.get("price"),
                "Status": data.get("status"),
                "SqFt": data.get("sqft"),
                "Days on Market": data.get("days_on_market")
            })
    
    return listings

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    if request.method == "POST":
        user_input = request.form.get("mls_ids")
        mls_ids = [mls.strip() for mls in user_input.split(",")]

        # Fetch real data from MLS API
        selected_listings = fetch_mls_data(mls_ids)

        if not selected_listings:
            report = "No matching listings found."
        else:
            total_price = sum(l["Price"] for l in selected_listings)
            avg_price = total_price / len(selected_listings) if selected_listings else 0
            min_price = min(l["Price"] for l in selected_listings)
            max_price = max(l["Price"] for l in selected_listings)
            avg_sqft = sum(l["SqFt"] for l in selected_listings) / len(selected_listings)
            avg_days_on_market = sum(l["Days on Market"] for l in selected_listings) / len(selected_listings)

            report = "🏡 **Real Estate Report** 🏡\n\n"

            for listing in selected_listings:
                report += f"📌 MLS ID: {listing['MLS ID']}\n"
                report += f"🏠 Address: {listing['Address']}\n"
                report += f"🛏 Beds: {listing['Beds']} | 🛁 Baths: {listing['Baths']}\n"
                report += f"💰 Price: ${listing['Price']:,}\n"
                report += f"📊 Status: {listing['Status']}\n"
                report += "-" * 40 + "\n"

            # Market Summary in Detailed Sentence Form
            market_summary = (
                f"\n📊 **Market Summary:**\n\n"
                f"🏠 There are **{len(selected_listings)} active listings** with prices ranging from **${min_price:,}** to **${max_price:,}**.\n"
                f"📉 The **average price** is **${avg_price:,.2f}**, and the average **square footage** is **{avg_sqft:,.0f} sqft**.\n"
                f"⏳ The **average days on market** is **{avg_days_on_market:.0f} days**.\n\n"
            )
            report += market_summary

    return render_template("index.html", report=report)

if __name__ == "__main__":
    app.run(debug=True)


