from FlightRadar24 import FlightRadar24API, FlightTrackerConfig

api = FlightRadar24API()

# api.set_flight_tracker_config(FlightTrackerConfig(limit="10"))
# flights = api.get_flights(
#     airline='CCU',
# )

# airports = api.get_airports() 
# print(airports)
airlines = api.get_airlines()
flights = api.get_flights()
lst = []
# zone = api.get_zones()["india"]
# print(flights)
# bounds = api.get_bounds(zone)
name="Boeing 767-3S2F"

for flight in flights:
    flight_details = api.get_flight_details(flight)
    flight.set_flight_details(flight_details)
    if  name == flight_details['aircraft']['model']['text']:
        print(flight_details)
        print("True")
        break
    # if flight.destination_airport_name != 'N/A':
    #     print(flight_details)
    #     print( flight_details['aircraft']['model']['text'])
    #     print(flight.latitude, flight.longitude)
    #     print("Flying from", flight.origin_airport_name)
    #     print("Flying to", flight.destination_airport_name)
    #     break
        # lst.append(flight.destination_airport_name)
        # lst.append(flight)  
        # break

# flight_details = api.get_flight_details("B763")
# flight.set_flight_details(flight_details)
# print(flight_details)

# print(flight)
# arr_flight_details = {}
# dept_flights_details={}
# airports = api.get_airports()
# airport_details = api.get_airport_details('CCU')
# print(airport_details)
# for flight in airport_details['airport']['pluginData']['schedule']['arrivals']['data']:
# # 
# #     # print(flight['flight']['aircraft']['model']['text'], flight['flight']['owner']['name'])
# #     # print(flight['flight']['airport']['origin']['name'])
# #     # print( flight['flight']['airport']['destination']['info']['name'])
#     print(flight)
#     break

# print(airport_details['airport']['pluginData']['schedule']['departures']['data'])

# Extracting required information

# arr_flight_details = []
# dept_flights_details=[]
# airports = api.get_airports()
# airport_details = api.get_airport_details('CCU')

# for flight in airport_details['airport']['pluginData']['schedule']['arrivals']['data']:
#     flight_info = {
#         'Aircraft Name':flight['flight']['aircraft']['model']['text'],
#         'Airline': flight['flight']['airline']['name'],
#         'Origin Airport': flight['flight']['airport']['origin']['name'],
#         'Destination Airport': "Kolkata Netaji Subhas Chandra Bose Airport",
#         'Terminal':flight['flight']['airport']['origin']['info']['terminal'],
#         'Delay': flight['flight']['status']['text'],
#         'Departure Time': flight['flight']['time']['scheduled']['departure'],
#         'Arrival Time': flight['flight']['time']['scheduled']['arrival']
#     }

#     arr_flight_details.append(flight_info)

# for flight in airport_details['airport']['pluginData']['schedule']['departures']['data']:
#     flight_info = {
#         'Aircraft Name': flight['flight']['aircraft']['model']['text'],
#         'Airline': flight['flight']['airline']['name'],
#         'Origin Airport': "Kolkata Netaji Subhas Chandra Bose Airport",
#         'Destination Airport': flight['flight']['airport']['destination']['name'],
#         'Terminal': flight['flight']['airport']['destination']['info']['terminal'],
#         'Status':  flight['flight']['status']['text'],
#         'Departure Time':  flight['flight']['time']['scheduled']['departure'],
#         'Departure Time': flight['flight']['time']['scheduled']['arrival']
#     }

#     dept_flights_details.append(flight_info)
