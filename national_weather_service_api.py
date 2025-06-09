import requests

"""
This script calls the National Weather Service API and extracts the location and detailed forcast of the weather 
from the returned json. This can be run as a stand alone script, or can be used when api_core.py runs.
"""

def call_api(coordinates: str) -> list:
    """
    This API has 2 steps. First you call the /points/ endpoint to receive metadata information
    about the cooridinates that you sent it. Then, using that metadata (gridID & forcast office's grid points),
    you call the /gridpoints/ endpoint to receive the weather data.
    """
    # Call the API to get necessary metadata needed for the forcast API call
    metadata_endpoint: str = 'https://api.weather.gov/points/'
    metadata_object: requests.Response = requests.get(metadata_endpoint + coordinates)


    # Start exception handling
    if metadata_object.status_code != 200:
        print("Reponse status code not 200")
        print(f"Status code: {metadata_object.status_code}")
        print("Check on the current availability of the National Weather Service API")
        return "\n"
    
    try:
        metadata_dict: dict = metadata_object.json()
    except requests.exceptions.JSONDecodeError:
        print("The API returned an object that was not valid JSON")
        print("Review your input and try the request again (Remember that the expected input is GPS coordinate decimal numbers with no more than 4 decimal points)")
        print(f"Response content type: {metadata_dict.headers["Content-Type"]}")
        return "\n"
    
    try:
        city: str = metadata_dict['properties']['relativeLocation']['properties']['city']
        state: str = metadata_dict['properties']['relativeLocation']['properties']['state']
        location: str = city +', ' + state
        gridId: str = metadata_dict['properties']['gridId']
        gridX: str = str(metadata_dict['properties']['gridX'])
        gridY: str = str(metadata_dict['properties']['gridY'])
    except KeyError:
        print(f"The API did not return any matches for the provided coordinates")
        print(f"Review your input and try the request again")
        
    # End exception handling


     # Call the API to get the weather forcast
    base_endpoint: str = 'https://api.weather.gov/gridpoints/'
    full_endpoint: str = base_endpoint +  gridId + '/' + gridX + ',' + gridY + '/' 'forecast'
    forecast_object: requests.Response = requests.get(full_endpoint)
    forecast_dict: dict = forecast_object.json()
    string_forcast: str = forecast_dict['properties']['periods'][0]['detailedForecast']

    return ['Location', location, 'Forcast', string_forcast]

if __name__ == '__main__':
    print('''+-----------------------------------------------------------------------------------------------------------------------------+
| This script reaches out to the National Weather Service API and returns a detailed forcast.                                 |
| It expects the {y,x }(latidute, longitude) coordinates of the location being searched.                                      |
| Example of expected input:                                                                                                  |
|    Enter the y coordinate:  47.0357 <-- the API does not support more than four decimal places of precision in coordinates  |
|    Enter the x coordinate:  -122.9048                                                                                       |
|                                                                                                                             |
+-----------------------------------------------------------------------------------------------------------------------------+\n\n''')
    while True:
        y_coordinate: str = input('Enter the y coordinates:\n ').strip()
        x_coordinate: str = input('Enter the x coordinates:\n ').strip()
        try:
            y: float = float(y_coordinate)
            x: float = float(x_coordinate)
            print('\n\n')
            pass
        except ValueError:
            print('You must enter decimal coordinates. Please try again.\n')
            del (y_coordinate, x_coordinate)
            continue

        joined_coordinates: str = ','.join([y_coordinate, x_coordinate])
        print(call_api(joined_coordinates))
