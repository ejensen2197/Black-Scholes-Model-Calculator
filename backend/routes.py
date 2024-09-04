from flask import Blueprint, request,jsonify
from .Data import BlackScholes, fetch_option_data
main = Blueprint('main', __name__)

@main.route('/api/data', methods=['GET'])
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)

@main.route('/api/send-data', methods=['POST'])
def send_data():
    data = request.json
    ticker = data["ticker"]
    strike_price = float(data["strike"])
    expiration_date = data["expiration"]
    option_type = data["option"]
    response = fetch_option_data(ticker,strike_price,expiration_date,option_type)
    #jsonify??
    return response