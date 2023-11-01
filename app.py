# Import packages
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import re
import sqlite3
import pandas as pd

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
    days = db.Column(db.Float, nullable=False)
    complete_meal = db.Column(db.String(20))
    number  = db.Column(db.Integer)
    ingredient = db.Column(db.String(1000))
    # Limited to 2 decimal places
    qualtity = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    measure = db.Column(db.String(20))
    type = db.Column(db.String(20))

@app.route("/", methods=['GET', 'POST'])
def home():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT number, name, ingredient, qualtity, measure, type FROM Recipes")
    all_recipes = cursor.fetchall()
    cursor.execute("SELECT number, name, days, complete_meal FROM Recipes")
    meta_info = cursor.fetchall()
    conn.close()
    
    all_recipes = group_data(all_recipes)
    meta_info = group_data(meta_info)
    for key in meta_info:
        meta_info[key] = list(set(meta_info[key]))

    if request.method == 'POST':
        selections = request.form['selectedItems']
        # Replace multiple spaces with a single space
        selections = re.sub(r'\s+', ' ', selections)
        selections = selections.replace('[','').replace(']','')
        # Replace colons, double quotes, and newline characters with nothing (remove them)
        selections = re.sub(r'[:"]', '', selections).split(r'\n')
        selections = [selection.strip() for selection in selections if (len(selection)>0) and ("-" not in selection) and ("?" not in selection) and ("," not in selection) and (selection != " ")]
        

        # Split the data into three separate lists
        ingredients = selections[::2]
        measures = selections[1::2]
        quantities = [float(quantity.split(' ')[0]) for quantity in measures]
        units = []
        ingredients_type = []
        for unit in measures:
            if len(unit.split(' '))==3:
                units.append((unit.split(' ')[1]))
                ingredients_type.append((unit.split(' ')[2]))
            else:
                units.append(f"{unit.split(' ')[1]} {unit.split(' ')[2]}")
                ingredients_type.append((unit.split(' ')[3]))

        shopping_list_df = pd.DataFrame({"ingredients": ingredients, "quantities": quantities, "units": units, "type": ingredients_type})
        shopping_list_df = shopping_list_df.groupby(['ingredients', 'units', 'type']).sum().reset_index()
        
        return jsonify(ingredients=list(shopping_list_df['ingredients']),quantities=list(shopping_list_df['quantities']), units=list(shopping_list_df['units']), ingredients_type=list(shopping_list_df['type']))

    return render_template("shopping_list.html", all_recipes=all_recipes, meta_info=meta_info)

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

        # Extract the number of days
        if not request.form['day']:
            number_days = 1
        else:
            number_days = request.form['day'].title()

        # Extract if it is a complete meal
        complete_meal_input = request.form['complete']

        # Extract ingredient inputs
        ingredients = request.form['ingredient'].split(",")
        ingredients_cleaned = [0 if ingredient == "" else ingredient for ingredient in ingredients]

        # Extract quantity inputs
        quantities = request.form['quantity'].split(",")
        quantities_cleaned = [0 if quantity == "" else quantity for quantity in quantities]

        # Extract measure type inputs
        measures = request.form['measure'].split(",")

        # Extract ingredient type
        type_inputs = request.form['type'].split(",")

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

        # Combine all information for each ingredient and remove any which contains 0 (missing ingredient or quantity)
        combined_inputs = []
        for ingredient, quantity, measure, type_input in zip(ingredients_cleaned, quantities_cleaned, measures, type_inputs):
            if ingredient != 0 and quantity != 0:
                combined_inputs.append([ingredient.capitalize().strip(), round(float(quantity),2), measure, type_input])
        
        #  Update db
        if len(combined_inputs) > 0:
            for combined_input in combined_inputs:
                new_upload = Recipes(name = recipe_name,days = number_days,complete_meal = complete_meal_input,number = highest_number, ingredient = combined_input[0], qualtity = combined_input[1], measure = combined_input[2], type = combined_input[3])
                db.session.add(new_upload)
                db.session.commit()



    return render_template("new_recipe.html")

@app.route("/modifyrecipe/")
def modifyrecipe():
    return render_template("modify_recipe.html")

def group_data(data):
    grouped_data = {}
    for item in data:
        key = '_'.join([str(item[0]), str(item[1])])
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(item[2:])  # Exclude the key from the item
    return grouped_data

if __name__ == "__main__":
    app.run(debug=True)