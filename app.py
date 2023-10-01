# Import packages
from flask import Flask, render_template

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("shopping_list.html")

@app.route("/stock/")
def stock():
    return render_template("stock.html")

if __name__ == "__main__":
    app.run(debug=True)