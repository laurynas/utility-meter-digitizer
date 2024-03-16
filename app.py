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
    decimals = request.args.get('decimals', default=0, type=int)
    data = request.get_data()
    image = Image.open(BytesIO(data))
    reading = digitizer.detect_string(image)
    value = float(reading) / (10 ** decimals)
    return json.dumps({'value': value}), 200, {'Content-Type': 'application/json'}

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

    json_data = json.dumps({'value': value})

    with open(json_file, 'w') as f:
        f.write(json_data)

    image.save(os.path.join(data_dir, f'{meter_id}.jpg'))

    return json_data, 200, {'Content-Type': 'application/json'}

@app.route('/meter/<identifier:meter_id>', methods=['GET'])
def show_meter(meter_id):
    json_file = os.path.join(data_dir, f'{meter_id}.json')
    if not os.path.exists(json_file):
        return 'Meter not found', 404
    with open(json_file, 'r') as f:
        return f.read(), 200, {'Content-Type': 'application/json'}

@app.route('/meter/<identifier:meter_id>/image', methods=['GET'])
def meter_image(meter_id):
    image_path = os.path.join(data_dir, f'{meter_id}.jpg')
    if not os.path.exists(image_path):
        return 'Meter not found', 404
    return open(image_path, 'rb').read(), 200, {'Content-Type': 'image/jpeg'}

@app.route('/meter/<identifier:meter_id>/reset', methods=['GET'])
def reset_meter(meter_id):
    value = request.args.get('value', type=float)
    json_file = os.path.join(data_dir, f'{meter_id}.json')
    image_file = os.path.join(data_dir, f'{meter_id}.jpg')
    
    if os.path.exists(json_file):
        os.remove(json_file)
    
    if os.path.exists(image_file):
        os.remove(image_file)

    if value is not None:
        json_data = json.dumps({'value': value})
        with open(json_file, 'w') as f:
            f.write(json_data)

    return 'Meter reset', 200
