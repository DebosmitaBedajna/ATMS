from FlightRadar24 import FlightRadar24API, FlightTrackerConfig

api = FlightRadar24API()

api.set_flight_tracker_config(FlightTrackerConfig(limit="5"))
flights = api.get_flights()

for flight in flights:
    flight.set_flight_details(api.get_flight_details(flight))
    print(flight.latitude+360, flight.longitude+360)
    break