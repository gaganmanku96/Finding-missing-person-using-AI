import logging

from flask import Flask, request, jsonify

from face_recognition_api import get_encoding

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        base64_image = request.get_json(force=True)
        result = get_encoding(base64_image)
        return jsonify(result)
    except Exception as e:
        logging.info("Something went wrong" + str(e))
        return None
