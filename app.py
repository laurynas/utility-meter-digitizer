import os
import json
from PIL import Image
from src.digitizer import Digitizer
from src.routing import IdentifierConverter
from src.draw import draw_objects
from io import BytesIO
from glob import glob
from flask import Flask, request

model = 'models/yolov8-detect-20240229.onnx'
data_dir = 'data/'

digitizer = Digitizer(model)

app = Flask(__name__)
app.url_map.converters['identifier'] = IdentifierConverter

@app.route('/digitize', methods=['POST'])
def digitize():
    value, _, _ = _detect()
    json_data = json.dumps({'value': value})

    return json_data, 200, {'Content-Type': 'application/json'}

@app.route('/meter/<identifier:meter_id>', methods=['POST'])
def update_meter(meter_id):
    value, objects, image = _detect()

    json_file = os.path.join(data_dir, f'{meter_id}.json')
    max_increase = request.args.get('max_increase', default=float('inf'), type=float)
    
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

    draw_objects(image, objects)

    image.save(os.path.join(data_dir, f'{meter_id}_result.jpg'))

    return json_data, 200, {'Content-Type': 'application/json'}

@app.route('/meter/<identifier:meter_id>', methods=['GET'])
def show_meter(meter_id):
    return _send_file(f'{meter_id}.json', 'application/json')

@app.route('/meter/<identifier:meter_id>/image', methods=['GET'])
def meter_image(meter_id):
    return _send_file(f'{meter_id}.jpg', 'image/jpeg')

@app.route('/meter/<identifier:meter_id>/image_result', methods=['GET'])
def meter_image_result(meter_id):
    return _send_file(f'{meter_id}_result.jpg', 'image/jpeg')

@app.route('/meter/<identifier:meter_id>/reset', methods=['GET'])
def reset_meter(meter_id):
    for file in glob(f'{data_dir}{meter_id}.*'):
        os.remove(file)

    value = request.args.get('value', default=None, type=float)

    if value is not None:
        json_data = json.dumps({'value': value})
        json_file = os.path.join(data_dir, f'{meter_id}.json')
        with open(json_file, 'w') as f:
            f.write(json_data)

    return 'Meter reset', 200

def _detect():
    decimals = request.args.get('decimals', default=0, type=int)
    data = request.get_data()
    image = Image.open(BytesIO(data))
    reading, objects = digitizer.detect(image)
    value = float(reading) / (10 ** decimals)

    return value, objects, image

def _send_file(file_name, content_type):
    path = os.path.join(data_dir, file_name)
    
    if not os.path.exists(path):
        return 'Meter not found', 404
    
    data = open(path, 'rb').read()

    return data, 200, {'Content-Type': content_type}