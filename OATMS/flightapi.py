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
# print(zone)
# bounds = api.get_bounds(zone)

for flight in flights:
    flight_details = api.get_flight_details(flight)
    flight.set_flight_details(flight_details)
    if flight.destination_airport_name != 'N/A':
        # print( flight_details['aircraft']['model']['text'])
        # print(flight.latitude, flight.longitude)
        # print("Flying from", flight.origin_airport_name)
        # print("Flying to", flight.destination_airport_name)
        # break
        # # lst.append(flight.destination_airport_name)
        lst.append(flight)  
        break


print(flight)


