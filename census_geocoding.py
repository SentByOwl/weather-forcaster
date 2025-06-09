import requests

"""
This script retrieves the coordinates of a given address using the US Census geocoding API.
It expects a full US address.
This modules api_api() method will return coordinates as {y,x} (Latidtude, Longitude). 
This is because the National Weather Service API expects coordinates to be Latidtude, Longitutude in their call.
This can be run as a stand alone script, or can be used when api_core.py runs.
"""

def remove_excess_decimal_numbers(y_coordinate: str, x_coordinate: str) -> str:
    """
    The function take both the x and y coordinates and shortens length of the decimals to 4 decimal places.
    The 4 decimal length is a limitation of the National Weather Service API.
    """
     # This group removes the extra decimals from the y coordinate. It leaves only 4 decimal places.
    y_coordinate_separated: list = y_coordinate.split('.')
    y_coordinate_whole: list = y_coordinate_separated[0]
    y_coordinate_decimals: list = y_coordinate_separated[1]
    y_coordinate_decimals_shortened: str = str(y_coordinate_decimals[slice(0, 4)])
    y_coordinate_fixed: str = str(y_coordinate_whole) + '.' + y_coordinate_decimals_shortened

    # This group removes the extra decimals from the x coordinate. It leaves only 4 decimal places.
    x_coordinate_separated: list = x_coordinate.split('.')
    x_coordinate_whole: list = x_coordinate_separated[0]
    x_coordinate_decimals: list = x_coordinate_separated[1]
    x_coordinate_decimals_shortened: str = str(x_coordinate_decimals[slice(0, 4)])
    x_coordinate_fixed: str = str(x_coordinate_whole) + '.' + x_coordinate_decimals_shortened
    shortened_coordinates: list = [y_coordinate_fixed, x_coordinate_fixed]
    return shortened_coordinates

def call_api(address: str) -> list:
    """
    Calls the US Census geocoding api to get the coordinates given a valid United States address.
    """
    # Format the address so that it can be accepted by the US Census geocoding API
    address_replace_spaces: str = address.replace(' ', '+')
    address_replace_commas: str = address_replace_spaces.replace(',', '%2C')
    url: str = f'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={address_replace_commas}&benchmark=4&format=json'
    geocode_object: requests.Response = requests.get(url)


    # Start exception handling
    if geocode_object.status_code != 200:
        exception_message: list = ["Reponse status code not 200", f"Status code: {geocode_object.status_code}", "Check on the availability of the US Census geocoder API"]
        return exception_message
    
    try:
        geocode_dict: dict = geocode_object.json()
    except requests.exceptions.JSONDecodeError:
        exception_message: list = ["message",  "The API returned an object that was not valid JSON. Review your input and try the request again (Remember that the expected input is a full US address)"]
        return exception_message
    
    try:
        x_coordinate: str = str(geocode_dict['result']['addressMatches'][0]['coordinates']['x'])
        y_coordinate: str = str(geocode_dict['result']['addressMatches'][0]['coordinates']['y'])
    except IndexError:
        exception_message: dict = {"message" : f"The API did not return any matches for the provided address. Review your input and try the request again"}
        return exception_message
    # End exception handling


    return remove_excess_decimal_numbers(y_coordinate, x_coordinate)

if __name__ == '__main__':
    address: str = input('Enter address to receive its coordinates {y,x} (Latitude,Longitude): ')
    print(call_api(address))
