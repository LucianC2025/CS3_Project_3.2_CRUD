from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drinks.db'
db = SQLAlchemy(app)

# make your own drink game 
# Look at javascript for dynmaic page changes 

class Drink(db.Model):
    # ID column
    id = db.Column(db.Integer, primary_key=True)
    # NAME column
    name = db.Column(db.String(100), nullable=False)
    # NOTE: PickleType: Holds Python objects, which are serialized using pickle.
    ingredients = db.Column(db.PickleType, nullable = False)

    # NOTE: __init__ : A constructor. Used to define how an object is created before storing it in the database
    def __init__(self, name, ingredients):
        if len(ingredients) > 50:
            raise ValueError('Stop. No more ingredients.')
        self.name = name
        self.ingredients = ingredients

# POST - ADD
@app.route('/add_drink', methods=["POST"])
def add_drink():
 