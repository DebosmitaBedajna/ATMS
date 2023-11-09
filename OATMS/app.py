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

def weatherData():
    #url = "https://api.weatherapi.com/v1/current.json?key=2eb13cf49a934aabb3b74217230611&q=Kolkata&aqi=yes"
    #data = post(url)

    return jsonify({}) #data.json()

@app.route('/profile')
def profile():
    return render_template('profile.html')

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

@app.route('/arrivals_departures')
def arrivals_departures():
    arrival_flight_details = get_arrivals()
    departure_flight_details = get_departures()
    return render_template('arrivals_departures.html', arr_flight_details=arrival_flight_details, dept_flights_details=departure_flight_details)


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

arr_flight_details = []
dept_flights_details=[]
airports = api.get_airports()
airport_details = api.get_airport_details('CCU')
def get_arrivals():

    for flight in airport_details['airport']['pluginData']['schedule']['arrivals']['data']:
        flight_info = {
            'Aircraft Name':flight['flight']['aircraft']['model']['text'],
            'Airline': flight['flight']['airline']['name'],
            'Origin Airport': flight['flight']['airport']['origin']['name'],
            'Destination Airport': "Kolkata Netaji Subhas Chandra Bose Airport",
            'Terminal':flight['flight']['airport']['origin']['info']['terminal'],
            'Delay': flight['flight']['status']['text'],
            'Departure Time': flight['flight']['time']['scheduled']['departure'],
            'Arrival Time': flight['flight']['time']['scheduled']['arrival']
        }

        arr_flight_details.append(flight_info)


    return  arr_flight_details


def get_departures():
    for flight in airport_details['airport']['pluginData']['schedule']['departures']['data']:
        flight_info = {
            'Aircraft Name': flight['flight']['aircraft']['model']['text'],
            'Airline': flight['flight']['airline']['name'],
            'Origin Airport': "Kolkata Netaji Subhas Chandra Bose Airport",
            'Destination Airport': flight['flight']['airport']['destination']['name'],
            'Terminal': flight['flight']['airport']['destination']['info']['terminal'],
            'Status':  flight['flight']['status']['text'],
            'Departure Time':  flight['flight']['time']['scheduled']['departure'],
            'Departure Time': flight['flight']['time']['scheduled']['arrival']
        }

        dept_flights_details.append(flight_info)

    return dept_flights_details

def perform_search(search_input):
    search_results = []

    for flight in arr_flight_details:
        if search_input.lower() in flight['Aircraft Name'].lower() or search_input.lower() in flight['Airline'].lower():
            search_results.append(flight)

    for flight in dept_flights_details:
        if search_input.lower() in flight['Aircraft Name'].lower() or search_input.lower() in flight['Airline'].lower():
            search_results.append(flight)

    return search_results

from flask import request, render_template

@app.route('/search', methods=['POST'])
def search():
    search_input = request.form.get('searchInput')
    search_results = perform_search(search_input)
    return render_template('arrivals_departures.html', arr_flight_details=arr_flight_details, dept_flights_details=dept_flights_details, search_results=search_results)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)