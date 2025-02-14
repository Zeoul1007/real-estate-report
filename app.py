from flask import Flask, render_template, request

app = Flask(__name__)

# Function to simulate fetching listing data
def get_real_estate_report(mls_ids):
    listings = {
        "40687604": {"address": "123 Main St, New York, NY", "beds": 3, "baths": 2, "price": "$550,000", "status": "Active", "sqft": 1500, "days_on_market": 30},
        "40692301": {"address": "456 Oak Ave, Los Angeles, CA", "beds": 4, "baths": 3, "price": "$720,000", "status": "Pending", "sqft": 1800, "days_on_market": 25}
    }
    
    selected_listings = [listings[mls] for mls in mls_ids if mls in listings]
    
    # Market Analysis
    active_listings = [l for l in selected_listings if l["status"] == "Active"]
    sold_listings = [l for l in selected_listings if l["status"] in ["Sold", "Closed"]]

    if active_listings:
        prices = [int(l["price"].replace("$", "").replace(",", "")) for l in active_listings]
        avg_price = sum(prices) / len(prices)
        avg_sqft = sum(l["sqft"] for l in active_listings) / len(active_listings)
        avg_days = sum(l["days_on_market"] for l in active_listings) / len(active_listings)
        market_summary = f"There are {len(active_listings)} active listings with prices ranging from ${min(prices):,} to ${max(prices):,}. The average price is ${avg_price:,.2f}, with an average square footage of {avg_sqft:.0f} sqft and an average days on market of {avg_days:.0f} days."
    else:
        market_summary = "No active listings found."

    if sold_listings:
        sold_prices = [int(l["price"].replace("$", "").replace(",", "")) for l in sold_listings]
        min_sold, max_sold = min(sold_prices), max(sold_prices)
        fastest_sale = min(l["days_on_market"] for l in sold_listings)
        longest_sale = max(l["days_on_market"] for l in sold_listings)
        sold_summary = f"There were {len(sold_listings)} closed listings with sale prices ranging from ${min_sold:,} to ${max_sold:,}. Fastest sale completed in {fastest_sale} days, longest sale took {longest_sale} days."
    else:
        sold_summary = "No closed listings found."

    return selected_listings, market_summary, sold_summary

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    if request.method == "POST":
        mls_input = request.form.get("mls_ids")
        if mls_input:
            mls_ids = mls_input.split(",")
            listings, market_summary, sold_summary = get_real_estate_report(mls_ids)
            report = {"listings": listings, "market_summary": market_summary, "sold_summary": sold_summary}
    return render_template("index.html", report=report)

if __name__ == "__main__":
    app.run(debug=True)




