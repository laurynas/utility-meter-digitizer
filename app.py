import os
from PIL import Image
from src.digitizer import Digitizer
from src.route_converters import IdentifierConverter
from io import BytesIO
from flask import Flask, request
import json

model = 'models/yolov8-detect-20240229.onnx'
data_dir = 'data/'

digitizer = Digitizer(model)

app = Flask(__name__)
app.url_map.converters['identifier'] = IdentifierConverter

@app.route('/digitize', methods=['POST'])
def digitize():
    data = request.get_data()
    image = Image.open(BytesIO(data))
    return digitizer.detect_string(image)

@app.route('/meter/<identifier:meter_id>', methods=['POST'])
def update_meter(meter_id):
    json_file = os.path.join(data_dir, f'{meter_id}.json')
    decimals = request.args.get('decimals', default=0, type=int)
    max_increase = request.args.get('max_increase', default=float('inf'), type=float)
    
    data = request.get_data()    
    image = Image.open(BytesIO(data))
    
    reading = digitizer.detect_string(image)
    value = float(reading) / (10 ** decimals)

    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        if value < data['value']:
            return 'Reading is lower than previous', 400
        if value - data['value'] > max_increase:
            return 'Reading increased too much', 400

    with open(json_file, 'w') as f:
        json.dump({'value': value}, f)

    image.save(os.path.join(data_dir, f'{meter_id}.jpg'))

    return str(value), 200, {'Content-Type': 'text/plain'}

@app.route('/meter/<identifier:meter_id>/image', methods=['GET'])
def meter_image(meter_id):
    image_path = os.path.join(data_dir, f'{meter_id}.jpg')
    if not os.path.exists(image_path):
        return 'Meter not found', 404
    return open(image_path, 'rb').read(), 200, {'Content-Type': 'image/jpeg'}
