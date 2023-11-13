from datetime import datetime
from flask import Flask, render_template, request, redirect, session
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from requests import post
from flask_migrate import Migrate
from datetime import timedelta
from FlightRadar24 import FlightRadar24API, FlightTrackerConfig
from flask_socketio import SocketIO, emit

api = FlightRadar24API()

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {
    'flights': 'sqlite:///flights.db'
}
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = 'secretivekeyagain'
curruser={}
app.config['SESSION_COOKIE_SECURE'] = True  
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1) 
socketio = SocketIO(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    designation = db.Column(db.String(80), default='ATC', nullable=True) 


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
        curruser['username'] = username
        curruser['designation'] = user.designation
        curruser['email'] = email
        curruser['password'] = password
        session['username'] = username
        return redirect('/dashboard')
    else:
        return render_template('login.html', error='Invalid credentials')


@app.route('/dashboard')
def dashboard():
    user=curruser
    wd = weatherData()
    print(wd)
    flight_data = get_flight_data()
    return render_template('dashboard.html', newvar=wd, flight_data=flight_data,user=user)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/') 


def weatherData():
    url = "https://api.weatherapi.com/v1/current.json?key=2eb13cf49a934aabb3b74217230611&q=Kolkata&aqi=yes"
    data = post(url)

    return data.json()

def create_user(username, email, password, designation):
    with app.app_context():
        user = User(username=username, email=email, password=password, designation=designation)
        db.session.add(user)
        db.session.commit()

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user=curruser
    print(user)
    if request.method == 'POST':
        action = request.form.get('action')

        if action == "addUser":
            new_username = request.form.get('username')
            new_email = request.form.get('email')
            new_password = request.form.get('password')
            new_designation = request.form.get('designation')
            
            if not new_username or not new_email or not new_password or not new_designation:
                flash('All fields are required for adding a user.', 'error')
                print("Validation error:", 'All fields are required for adding a user.')
            else:
                new_user = User(username=new_username, email=new_email, password=new_password, designation=new_designation)
                db.session.add(new_user)
                db.session.commit()
                flash(f'User {new_username} added successfully!', 'success')
                print(f'User {new_username} added successfully!')
                print("Received data:", new_username, new_email, new_password, new_designation)


        elif action == "removeUser":
            remove_username = request.form.get('removeUsername')
            user_to_remove = User.query.filter_by(username=remove_username).first()

            if user_to_remove:
                db.session.delete(user_to_remove)
                db.session.commit()
                flash(f'User {remove_username} removed successfully!', 'success')
            else:
                flash(f'User {remove_username} not found.', 'error')

    return render_template('profile.html', user=user)


@socketio.on('message')
def handle_message(msg):
    emit('message', msg, broadcast=True)


@app.route('/arrivals_departures')
def arrivals_departures():
    arrival_flight_details = get_arrivals()
    departure_flight_details = get_departures()
    scheduled_flights_data = get_scheduled_flights()
    return render_template('arrivals_departures.html', arr_flight_details=arrival_flight_details, dept_flights_details=departure_flight_details, scheduled_flights=scheduled_flights_data)


def get_flight_data():
    api.set_flight_tracker_config(FlightTrackerConfig(limit="30"))
    flights = api.get_flights()
    lst=[]
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

def create_user(username, email, password, designation):
    with app.app_context():
        user = User(username=username, email=email, password=password, designation=designation)
        db.session.add(user)
        db.session.commit()

@socketio.on('emergency')
def handle_emergency():
    emit('emergency_alert', broadcast=True)

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aircraft_name = db.Column(db.String(255), nullable=False)
    airline = db.Column(db.String(255), nullable=False)
    origin_airport = db.Column(db.String(255), nullable=False)
    destination_airport = db.Column(db.String(255), nullable=False)
    terminal = db.Column(db.String(10), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

@app.route('/schedule', methods=['POST'])
def schedule_flight():
    if request.method == 'POST':
        aircraft_name = request.form['aircraftName']
        airline = request.form['airline']
        origin_airport = request.form['originAirport']
        destination_airport = request.form['destinationAirport']
        terminal = request.form['terminal']
        departure_time = datetime.strptime(request.form['departureTime'], '%Y-%m-%dT%H:%M')
        arrival_time = datetime.strptime(request.form['arrivalTime'], '%Y-%m-%dT%H:%M')

        new_flight = Flight(
            aircraft_name=aircraft_name,
            airline=airline,
            origin_airport=origin_airport,
            destination_airport=destination_airport,
            terminal=terminal,
            departure_time=departure_time,
            arrival_time=arrival_time
        )
        db.session.add(new_flight)
        db.session.commit()

        return redirect('/arrivals_departures')
    
def get_scheduled_flights():
    scheduled_flights = Flight.query.all()

    scheduled_flights_data = [
        {
            'Aircraft Name': flight.aircraft_name,
            'Airline': flight.airline,
            'Origin Airport': flight.origin_airport,
            'Destination Airport': flight.destination_airport,
            'Terminal': flight.terminal,
            'Departure Time': flight.departure_time.strftime('%Y-%m-%dT%H:%M'), 
            'Arrival Time' : flight.arrival_time.strftime('%Y-%m-%dT%H:%M')
        }
        for flight in scheduled_flights
    ]

    return scheduled_flights_data
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
