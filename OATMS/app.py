from flask import Flask, render_template, request, redirect, session,jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from requests import post
import json

from FlightRadar24 import FlightRadar24API, FlightTrackerConfig

api = FlightRadar24API()

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/debosmitabedajna/Desktop/bkatms/OATMS/instance/users.db'
db = SQLAlchemy(app)
app.secret_key = 'secretivekeyagain'
chat_messages = []

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
 
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    user = User.query.filter_by(username=username, email=email, password=password).first()

    if user:
        return redirect('/dashboard')
    else:
        return render_template('login.html', error='Invalid credentials')


@app.route('/dashboard')
def dashboard():
    wd = weatherData()
    flight_data = get_flight_data()
    return render_template('dashboard.html', newvar=wd, flight_data=flight_data)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/') 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

def weatherData():
    #url = "https://api.weatherapi.com/v1/current.json?key=2eb13cf49a934aabb3b74217230611&q=Kolkata&aqi=yes"
    #data = post(url)

    return jsonify({}) #data.json()

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if 'username' in session:
        username = session['username']
        chat_messages.append(f'{username}: {message}')
    return jsonify({'status': 'success'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify({'messages': chat_messages})

def get_flight_data():
    api.set_flight_tracker_config(FlightTrackerConfig(limit="30"))
    flights = api.get_flights()
    lst = []
    for flight in flights:
        flight_details = api.get_flight_details(flight)
        flight.set_flight_details(flight_details)
        if flight.destination_airport_name != 'N/A':
            flight.name = flight_details['aircraft']['model']['text']
            lst.append(flight)  
    return lst
