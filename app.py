from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import json 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
# Flash Messages (this is required)
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)



# NOTE (to self): make your own drink game - Look at javascript for dynmaic page changes 


# ***** Drink CLASS *****
# NOTE: PickleType: Holds Python objects, which are serialized using pickle.
# NOTE: __init__ : A constructor. Used to define how an object is created before storing it in the database
# NOTE: Text(size) Holds a string with a maximum length of 65,535 bytes
class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False) 
    #Store the ingredients as a serialized list 
    ingredients = db.Column(db.PickleType, nullable = False)

    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
    
    def get_ingredients(self):
        return self.ingredients

# ***** End of Drink CLASS *****



# ********** ROUTES  **********
# NOTE: flash() is apart of Flask, and is used to send temporary messages to the user, like error notifications. The message is stored temporarly and dissapears shortly after being displayed
 # NOTE: flash('message', 'category') 
# Flask Route for displaying all tasks
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve data from the form in index.html
        name = request.form.get('name')
        #JSON string from ingredients_hidden input
        ingredients_json = request.form.get('ingredients')

        try:
            # Convert JSON string to python list
            ingredients_list = json.loads(ingredients_json) if ingredients_json else []
            # DEBUG
            print(f"Parsed ingredients list: {ingredients_list}")  
            # "Clean up" ingredients list 
            ingredients_list = [ingredient.strip() for ingredient in ingredients_list if ingredient.strip()]

            if not ingredients_list:
                flash("Please add at least one ingredient!")
                return redirect(url_for('index'))
            
            if not isinstance(ingredients_list, list):
                flash('Invalid ingredient input!', 'error')
                return redirect(url_for('index'))
            
        except json.JSONDecodeError:
            flash("Invalid ingredient input!", 'error')
            return redirect(url_for('index'))
     

        # Save to database
        if name and ingredients_list:
            new_drink = Drink(name=name, ingredients=ingredients_list)
            db.session.add(new_drink)
            db.session.commit()
            #flash(f'Succesfully added {name}!', 'success')
        else:
            flash("Please add a drink name and ingredients", 'error')
        return redirect("/")

    drinks = Drink.query.all()

    return render_template('index.html', drinks=drinks)
# ************ END OF def index(): ************

@app.route('/delete/<drink_id>', methods=['POST'])
def delete_drink(drink_id):
    drink = Drink.query.get_or_404(drink_id)
    db.session.delete(drink)
    db.session.commit()
    #flash(f'Deleted "{drink.name}" successfully!', 'success')
    return redirect(url_for('index'))



if __name__  == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port="1273", debug=True)