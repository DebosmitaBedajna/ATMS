from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User
from requests import post
import json

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/debosmitabedajna/Desktop/bkatms/OATMS/instance/users.db'
db = SQLAlchemy(app)
app.secret_key = 'secretivekeyagain'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
 
@app.route('/')
def index():
    weatherData()
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
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/') 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)

def weatherData():
    url = "https://api.weatherapi.com/v1/current.json?key=2eb13cf49a934aabb3b74217230611&q=Kolkata&aqi=yes"
    data = post(url)
    weatherdata = data.json()