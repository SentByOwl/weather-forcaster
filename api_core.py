from flask import Flask, jsonify, request
from main import RequestHandler, Logger

app = Flask(__name__)


@app.get("/forcast")
def get_forcast():
    # Get address components from query parameters
    street: str = request.args.get('street')
    city: str = request.args.get('city')
    state: str = request.args.get('state')
    zip_code: str = request.args.get('zip')

    # Check if any of the parameters are missing or empty
    for i in [street, city, state, zip_code]:
        if i is None or i == '':
            return jsonify({"error message":"Full address not recieved"})
    
    address: str = f"{street}{city} + '' + {state} + ', ' + {zip_code}"
    
    # Send the address to the main module to process it and return the forcast
    Request: RequestHandler = RequestHandler(address)
    forcast: list = Request.call_APIs()
    formated_forcast: dict = Request.format_data_as_dict(forcast)
    return formated_forcast
    
@app.get("/help")
def get_help():
    return jsonify({"Expected request example":"http://127.0.0.1:5000/forcast?street=1300+First+Avenue&city=Seattle&state=WA&zip=98101"})
