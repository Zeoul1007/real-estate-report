from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    report = """
    📊 **Market Summary:**

    There are **2 active listings** with prices ranging from **$424,900** to **$539,900**.
    The **average price** is **$482,400.00**, and the **average square footage** is **772 sq ft**.
    The **average days on market** is **22 days**.

    **Sold Listings**:
    - **1 closed listing** with sale prices ranging from **$422,681** to **$422,681**.
    - Fastest sale completed in **29 days**, longest sale took **29 days**.
    """
    return render_template("index.html", report=report)

if __name__ == '__main__':
    app.run(debug=True)



