# Import packages
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

# As the database created is found within the instance folder, the path is saved within a variable
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'database.db')

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] = ''
db = SQLAlchemy(app)

# The database was setup so that:
# The Recipes contains the recipies name, ingredients and qualtity
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    ingredient = db.Column(db.String(1000))
    # Limited to 2 decimal places
    qualtity = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

@app.route("/")
def home():
    return render_template("shopping_list.html")

@app.route("/stock/")
def stock():
    return render_template("stock.html")

@app.route("/newrecipe/")
def newrecipe():
    return render_template("new_recipe.html")

@app.route("/modifyrecipe/")
def modifyrecipe():
    return render_template("modify_recipe.html")

if __name__ == "__main__":
    app.run(debug=True)