from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User  # Assuming your User model is defined in 'models.py'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/debosmitabedajna/Desktop/bkatms/OATMS/instance/users.db'
db = SQLAlchemy(app)

# Function to create a user
def create_user(username, email, password):
    with app.app_context():
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    create_user("JohnDoe", "johndoe@example.com", "mypassword123")
