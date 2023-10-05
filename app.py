# Import packages
from flask import Flask, render_template, request
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
    number  = db.Column(db.Integer)
    ingredient = db.Column(db.String(1000))
    # Limited to 2 decimal places
    qualtity = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    measure = db.Column(db.String(20))

@app.route("/")
def home():
    return render_template("shopping_list.html")

@app.route("/stock/")
def stock():
    return render_template("stock.html")

@app.route("/newrecipe/", methods=['GET', 'POST'])
def newrecipe():
    # If the submit button is activated
    if request.method == 'POST':
        # Extract the recipe name (in no name given, the name is assigned "Unnamed recipe")
        if not request.form['recipe']:
            recipe_name = "Unnamed Recipe"
        else:
            recipe_name = request.form['recipe'].title()
        print(recipe_name)

        # Extract ingredient inputs
        ingredients = request.form['ingredient'].split(",")
        ingredients_cleaned = [0 if ingredient == "" else ingredient for ingredient in ingredients]

        # Extract quantity inputs
        quantities = request.form['quantity'].split(",")
        quantities_cleaned = [0 if quantity == "" else quantity for quantity in quantities]

        # Extract measure type inputs
        measures = request.form['measure'].split(",")

        # Extract current highest recipe number and add 1 (incase there is multiple recipes with the same name)
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT number FROM Recipes")
        highest_number = cursor.fetchall()
        conn.close()
        try:
            highest_number = max(highest_number, key=lambda x: x[0])[0]
            highest_number+=1
        except:
            highest_number = 0
        print(highest_number)

        # Combine all information for each ingredient and remove any which contains 0 (missing ingredient or quantity)
        combined_inputs = []
        for ingredient, quantity, measure in zip(ingredients_cleaned, quantities_cleaned, measures):
            if ingredient != 0 and quantity != 0:
                combined_inputs.append([ingredient.capitalize().strip(), round(float(quantity),2), measure])

        print(combined_inputs)
        
        #  Update db
        if len(combined_inputs) > 0:
            for combined_input in combined_inputs:
                print(combined_input)
                new_upload = Recipes(name = recipe_name,number = highest_number, ingredient = combined_input[0], qualtity = combined_input[1], measure = combined_input[2])
                db.session.add(new_upload)
                db.session.commit()



    return render_template("new_recipe.html")

@app.route("/modifyrecipe/")
def modifyrecipe():
    return render_template("modify_recipe.html")

if __name__ == "__main__":
    app.run(debug=True)