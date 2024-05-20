# **Air Traffic Management System (ATMS)**


## **Overview**

The Air Traffic Management System (ATMS) is a software solution designed to efficiently and safely manage the movement of aircraft within designated airspace. This system leverages a Database Management System (DBMS) to organize, retrieve, and manage critical flight data, ensuring real-time tracking and resource allocation.

## **Features**
- Real-time Flight Tracking: Monitor aircraft position, altitude, speed, and heading angle in real time.
- Entity Representation: Comprehensive management of pilots, aircraft, weather reports, airports, and runways.
- Flight Categorization: Flexible handling of domestic and international flights through generalization/specialization.
- Resource Allocation: Efficient allocation and reallocation of airport resources like terminals and runways.
- Weather Information: Real-time weather updates for specific locations to aid in flight planning.
- Communication System: Real-time messaging for seamless coordination between pilots and air traffic controllers.

## **Requirements**
- Python 3.x
- Flask
- SQLAlchemy

## **Installation**

#### Clone the repository:
```
git clone https://github.com/yourusername/atms.git
cd atms
```
#### Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate
```
#### Install dependencies:
```
pip install -r requirements.txt
```
#### Start the server:
```
flask run
```
Access the application at http://localhost:5000.

## Contributing
- Fork the repository.
- Create a new branch
```
  git checkout -b feature-branch
```
- Make your changes and commit them
  ```
  git commit -m 'Add new feature'
  ```
- Push to the branch
  ```
  git push origin feature-branch
  ```
- Create a new Pull Request.
