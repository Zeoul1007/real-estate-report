from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    if request.method == "POST":
        listing_ids = request.form.get("listing_ids").split(",")
        report = generate_real_estate_report(listing_ids)
    
    return render_template("index.html", report=report)

def generate_real_estate_report(listing_ids):
    # Mock database of MLS listings
    listings = {
        "40687604": {"address": "123 Main St, New York, NY", "beds": 3, "baths": 2, "price": 550000, "status": "Active", "sqft": 1500, "days_on_market": 30},
        "40692301": {"address": "456 Oak Ave, Los Angeles, CA", "beds": 4, "baths": 3, "price": 720000, "status": "Pending", "sqft": 1800, "days_on_market": 45},
    }
    
    selected_listings = [listings[lid] for lid in listing_ids if lid in listings]

    if not selected_listings:
        return "No matching listings found."

    # Market Analysis
    active_listings = [l for l in selected_listings if l["status"] == "Active"]
    closed_listings = [l for l in selected_listings if l["status"] in ["Closed", "Sold"]]

    analysis = {
        "active_count": len(active_listings),
        "closed_count": len(closed_listings),
        "price_range": (min([l["price"] for l in selected_listings]), max([l["price"] for l in selected_listings])),
        "avg_price": sum([l["price"] for l in selected_listings]) / len(selected_listings),
        "avg_sqft": sum([l["sqft"] for l in selected_listings]) / len(selected_listings),
        "avg_days_on_market": sum([l["days_on_market"] for l in selected_listings]) / len(selected_listings),
    }

    # Report Summary
    report = f"""
    📊 **Market Analysis:**
    📌 **Active Listings Summary:**
    - {analysis['active_count']} Active Listings
    - Price range: ${analysis['price_range'][0]:,} - ${analysis['price_range'][1]:,}
    - **Avg Price:** ${analysis['avg_price']:.2f}
    - **Avg Square Footage:** {analysis['avg_sqft']:.0f} sqft
    - **Avg Days on Market:** {analysis['avg_days_on_market']:.1f} days
    """

    return report

if __name__ == "__main__":
    app.run(debug=True)


