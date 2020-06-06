from flask import Flask, request, jsonify
from catboost import CatBoost

import logging
import traceback
from logging.handlers import RotatingFileHandler
from time import strftime, time

from process_data import process_input


app = Flask(__name__)


claims_count_model = CatBoost().load_model("models/ClaimsCount_model.cbm", format="cbm")
avg_claim_model = CatBoost().load_model("models/AvgClaim_model.cbm", format="cbm")

# Logging
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route("/")
def index():
    return "API for predict service"


@app.route("/predict", methods=["POST"])
def predict():

    json_input = request.json

    # Request logging
    current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)
    logger.info(f'{current_datatime} request from {ip_address}: {request.json}')
    start_prediction = time()
    id = json_input["ID"]
    data = process_input(json_input)
    prediction_claims_count = claims_count_model.predict(data)
    prediction_avg_claim = avg_claim_model.predict(data)

    value_burning_cost = prediction_claims_count * prediction_avg_claim

    result = {"ID": id,
              "prediction_claims_count": prediction_claims_count,
              "prediction_avg_claim": prediction_avg_claim,
              "value_burning_cost": value_burning_cost
              }

    # Response logging
    end_prediction = time()
    duration = round(end_prediction - start_prediction, 6)
    current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
    logger.info(f'{current_datatime} predicted for {duration} msec: {result}\n')

    return jsonify(result)


@app.errorhandler(Exception)
def exceptions(e):
    current_datatime = strftime('[%Y-%b-%d %H:%M:%S]')
    error_message = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                 current_datatime,
                 request.remote_addr,
                 request.method,
                 request.scheme,
                 request.full_path,
                 error_message)
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
