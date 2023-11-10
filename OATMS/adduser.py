from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/debosmitabedajna/Desktop/bkatms/OATMS/instance/users.db'
db = SQLAlchemy(app)
app.app_context().push()  
# def update_user_designation(username, new_designation):
#     with app.app_context():
#         user = User.query.filter_by(username=username).first()

#         if user:
#             user.designation = new_designation
#             db.session.commit()
#             print(f"Designation updated for user {username}: {new_designation}")
#         else:
#             print(f"User {username} not found.")

# if __name__ == "__main__":
#     update_user_designation("JohnDoe", "ATC")
# Function to create a user
def create_user(username, email, password, designation):
    with app.app_context():
        user = User(username=username, email=email, password=password, designation=designation)
        db.session.add(user)
        db.session.commit()

if __name__ == '__main__':
    create_user("JaneDoe", "janedoe@example.com", "mypassword123", "Pilot")