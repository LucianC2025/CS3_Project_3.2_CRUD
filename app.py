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
class Drink(db.Model):
    # NOTE: PickleType: Holds Python objects, which are serialized using pickle.
    # NOTE: __init__ : A constructor. Used to define how an object is created before storing it in the database
    # NOTE: Text(size) Holds a string with a maximum length of 65,535 bytes

    id = db.Column(db.Integer, primary_key=True)
    # Store the ingredients as a serialized list 
    ingredients = db.Column(db.PickleType, nullable = False)
    name = db.Column(db.Text, nullable=False) 

    # Goal: esure that the ingredients are a list.. I want the code on the HTML file to appear as a bulleted list.. but I want the ingredients to be stored in the dataframe as a list.. 
    def __init__(self, name, ingredients):
        if not isinstance(ingredients, list):
            raise ValueError('Ingredients must be a list.')
        if len(ingredients) >= 50:
            raise ValueError('Stop. Too many ingredients!!!')
        if len(ingredients) >= 20:
            print('Calm down there...')

        self.name = name
        # NOTE: json.dumps() stores a serialized list as a JSON string
        self.ingredients = json.dumps(ingredients) 
    
    def get_ingredients(self):
        # Turn the JSON string back into a list for python purposes
        return json.loads(self.ingredients)

# ***** End of Drink CLASS *****




# Flask Route for displaying all tasks

# GOAl: When you add ingredients it should be a bullet list below the [] box and not create another box
@app.route('/', methods=['GET', 'POST'])
def index():
    # ***** POST (add) method ******
    if request.method == 'POST':
        name = request.form.get('name')
        ingredients = request.form.getlist('ingredients[]')

        # NOTE: flash() is apart of Flask, and is used to send temporary messages to the user, like error notifications. The message is stored temporarly and dissapears shortly after being displayed
        # NOTE: flash('message', 'category') 
        # NOTE: url_for() looks for the flask route function not the file. 
            #For example  url_for('index') looks for the Flask route function index not the HTML file index.html

        if not name or not ingredients: 
            flash('Please enter a name and at least one ingredient', 'error')
            return redirect(url_for('index'))
        
        if len(ingredients) >=50: 
            flash('Too many ingredients! Maximum allowed is 50.', 'error')
            return redirect(url_for('index'))
        
        new_drink = Drink(name, ingredients)
        db.session.add(new_drink)
        db.session.commit()
        flash("Drink created sucessfully!", "success")

        return redirect(url_for('index'))
    # ***** end of POST (add) method ******

    drinks = Drink.query.all()
    return render_template('index.html', drinks = drinks)
 #***** end of INDEX function ******
     


if __name__  == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port="1117", debug=True)