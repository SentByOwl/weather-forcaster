import census_geocoding
import national_weather_service_api
import json

"""
Define a few classes that contain the methods needed to get the weather data.
The classes will be instantiated in api_core.py.
"""

class RequestHandler:
    """
    All actions on the request data will be initiated using one of the methods defined here.
    """
    def __init__(self, address: str):
        self.address: str = address
    
    def call_APIs(self) -> list:
        coordinates: list = census_geocoding.call_api(self.address)
        coordinates: str = ','.join(coordinates)
        forcast: list = national_weather_service_api.call_api(coordinates)
        return forcast

    @staticmethod
    def format_data_as_dict(forcast_list: list) -> dict:
        """
        Receive final weather data from and format it into JSON 
        to be sent back to the client
        """
        location, location_string, forcast, forcast_string = forcast_list

        new_dict: dict = {
            location : location_string,
            forcast : forcast_string
            }
        return new_dict



class Logger:
    """
    Not used yet
    """
    def __init__(self, client_metadata: dict, server_metadata: dict):
        self.client_metadata = client_metadata
        self.server_metadata = server_metadata



if __name__ == "__main__":
    raise Exception("This file must be run as a module imported by api_core.py")



'''
I'm converting this into an api and away from a commandline tool. I should place these cli components in their own class that can be used if I want to run this from the cli
print('\n--Pull weather data from the National Weather Service API--\n')
address: str = input('Enter the address that you want weather data from: \n')
# Use the US Census geocoding API to get the coordinates from an Address
coordinates: list = census_geocoding.call_api(address)
# Join these to a list so that we can pass it to the national_weather_service_api.call_api()
coordinates: str = ','.join(coordinates)
# Finally we pass those coordinates to national_weather_service_api.call_api() and return
# the detailed forcast of the current weather
weather_data: list = national_weather_service_api.call_api(coordinates)
weather_data_dict: dict = format_data_as_dict(weather_data)
weather_data_json: str =  json.dumps(weather_data_dict)
print(weather_data_json)
'''