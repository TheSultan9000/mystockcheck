# Import packages
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import re
import sqlite3
import pandas as pd
import webbrowser


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
    group = db.Column(db.Integer)
    ingredient = db.Column(db.String(1000))
    # Limited to 2 decimal places
    qualtity = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    measure = db.Column(db.String(20))
    type = db.Column(db.String(20))

@app.route("/", methods=['GET', 'POST'])
def home():
    all_recipes, meta_info = db_all_recipes()
    if request.method == 'POST':
        request_type = request.form['request_type']
        if request_type == 'shopping_list':
            selections = request.form['selectedItems']
            # Replace multiple spaces with a single space
            selections = re.sub(r'\s+', ' ', selections)
            selections = selections.replace('[','').replace(']','')
            # Replace colons, double quotes, and newline characters with nothing (remove them)
            selections = re.sub(r'[:"]', '', selections).split(r'\n')
            recipe_list = [selection.replace("-", "").strip() for selection in selections if (len(selection)>0) and ("-" in selection) and ("days" not in selection)  and ("Group" not in selection)]
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
            
            return jsonify(recipe_list = recipe_list, ingredients=list(shopping_list_df['ingredients']),quantities=list(shopping_list_df['quantities']), units=list(shopping_list_df['units']), ingredients_type=list(shopping_list_df['type']))
        elif request_type == 'modify_recipe':
            recipe_to_modify = request.form['button']
            return jsonify(recipe_to_modify)
        elif request_type == 'delete_recipe':
            recipe_to_delete = request.form['button'].split("_")[0]
            # Delete the rows with the recipe number
            # Connect to the SQLite database
            conn = sqlite3.connect('instance/database.db')
            cursor = conn.cursor()
            # Execute the DELETE query
            cursor.execute("DELETE FROM Recipes WHERE number = ?", (recipe_to_delete,))
            # Commit the transaction to save the changes
            conn.commit()
            # Close the database connection
            conn.close()

    return render_template("shopping_list.html", all_recipes=all_recipes, meta_info=meta_info)

@app.route("/<recipe_to_modify>/", methods=['GET', 'POST'])
def recipetomodify(recipe_to_modify):
    if recipe_to_modify != 'favicon.ico':
        recipe_name_to_modify = recipe_to_modify.split("_")[2]
        recipe_number_to_modify = recipe_to_modify.split("_")[1]
        all_recipes, meta_info = db_all_recipes()
        all_recipes = all_recipes[recipe_to_modify]
        meta_info = meta_info[recipe_to_modify][0]
        recipe_group = recipe_to_modify.split("_")[0]
        return render_template("modify_recipe.html", all_recipes=all_recipes, meta_info=meta_info, recipe_name = recipe_name_to_modify, recipe_number= recipe_number_to_modify, recipe_group = recipe_group)
    return ""

@app.route("/newrecipe/", methods=['GET', 'POST'])
def newrecipe():
    previous_ingredients = previousingredients()
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

        # Extract the group number
        if not request.form['group']:
            group_number = 0
        else:
            group_number = request.form['group'].title()

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
        
        # Update db
        # Ensures thaty the script is only run if there is at least on ingredient
        if len(combined_inputs) > 0:
            recipe_number_to_remove = request.form['button']
            if recipe_number_to_remove != "submit_new_recipe":
                # Delete the rows with the recipe number
                # Connect to the SQLite database
                conn = sqlite3.connect('instance/database.db')
                cursor = conn.cursor()
                # Execute the DELETE query
                cursor.execute("DELETE FROM Recipes WHERE number = ?", (recipe_number_to_remove,))
                # Commit the transaction to save the changes
                conn.commit()
                # Close the database connection
                conn.close()
            for combined_input in combined_inputs:
                new_upload = Recipes(name = recipe_name, days = number_days, group = group_number, complete_meal = complete_meal_input,number = highest_number, ingredient = combined_input[0], qualtity = combined_input[1], measure = combined_input[2], type = combined_input[3])
                db.session.add(new_upload)
                db.session.commit()

    return render_template("new_recipe.html", previous_ingredients = previous_ingredients)

def group_data(data):
    grouped_data = {}
    for item in data:
        key = '_'.join([str(item[0]), str(item[1]), str(item[2])])
        if key not in grouped_data:
            grouped_data[key] = []
        grouped_data[key].append(item[2:])  # Exclude the key from the item
    return grouped_data

def db_all_recipes():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT \"group\", number, name, ingredient, qualtity, measure, type FROM Recipes")
    all_recipes = cursor.fetchall()
    cursor.execute("SELECT \"group\", number, name, \"group\", days, complete_meal FROM Recipes")
    meta_info = cursor.fetchall()
    conn.close()
    
    all_recipes = group_data(all_recipes)
    meta_info = group_data(meta_info)
    for key in meta_info:
        meta_info[key] = list(set(meta_info[key]))

    return all_recipes, meta_info

def previousingredients():
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ingredient FROM Recipes")

    return [re.sub(r'[^a-zA-Z\s]', '', ingredient[0]) for ingredient in list(set(cursor.fetchall()))]

if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=False) # debug set to false otherwise two tabs will open when running the app