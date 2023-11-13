from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Flight(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    aircraft_name = db.Column(db.String(255), nullable=False)
    airline = db.Column(db.String(255), nullable=False)
    origin_airport = db.Column(db.String(255), nullable=False)
    destination_airport = db.Column(db.String(255), nullable=False)
    terminal = db.Column(db.String(50), nullable=True)
    delay = db.Column(db.String(50), nullable=True)
    departure_time = db.Column(db.String(50), nullable=False)
    arrival_time = db.Column(db.String(50), nullable=False)

# Assuming you have a Flask app instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flights.db'  # Use your actual database URI
db.init_app(app)

# # Create the table
# with app.app_context():
#     db.create_all()