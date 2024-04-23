import json
import base64
from PIL import Image
from src.digitizer import Digitizer
from src.routing import IdentifierConverter
from src.draw import draw_objects
from src.file_storage import FileStorage
from io import BytesIO
from glob import glob
from flask import Flask, request, send_file

model = 'models/yolov8-detect-20240229.onnx'
data_dir = 'data/'

digitizer = Digitizer(model)
storage = FileStorage(data_dir)

app = Flask(__name__)
app.url_map.converters['identifier'] = IdentifierConverter

@app.route('/digitize', methods=['POST'])
def digitize():
    decimals = request.args.get('decimals', default=0, type=int)
    threshold = request.args.get('threshold', default=0.7, type=float)
    
    image = __request_image()
    value, _ = digitizer.detect(image, decimals, threshold)

    if value is None:
        return 'No reading found', 400

    return json.dumps({'value': value}), 200, {'Content-Type': 'application/json'}

@app.route('/meter/<identifier:meter_id>', methods=['POST'])
def update_meter(meter_id):
    decimals = request.args.get('decimals', default=0, type=int)
    threshold = request.args.get('threshold', default=0.7, type=float)
    max_increase = request.args.get('max_increase', default=float('inf'), type=float)

    image = __request_image()
    value, objects = digitizer.detect(image, decimals, threshold)

    if value is None:
        return 'No reading found', 400

    try:
        old_value = storage.read_value(meter_id)

        if value < old_value:
            return 'Reading is lower than previous', 400
        if value - old_value > max_increase:
            return 'Reading increased too much', 400
    except FileNotFoundError:
        # no old value
        pass

    result_image = image.copy() 
    draw_objects(result_image, objects)
    
    storage.store(meter_id, value, image, result_image)

    return json.dumps({'value': value}), 200, {'Content-Type': 'application/json'}

@app.route('/meter/<identifier:meter_id>', methods=['GET'])
def show_meter(meter_id):
    try:
        value = storage.read_value(meter_id)
        return json.dumps({'value': value}), 200, {'Content-Type': 'application/json'}
    except FileNotFoundError:
        return 'Meter not found', 404

@app.route('/meter/<identifier:meter_id>/image', methods=['GET'])
def meter_image(meter_id):
    try:
        data = storage.read_image_data(meter_id)
        return data, 200, {'Content-Type': 'image/jpeg'} 
    except FileNotFoundError:
        return 'Meter not found', 404

@app.route('/meter/<identifier:meter_id>/result_image', methods=['GET'])
def meter_result_image(meter_id):
    try:
        data = storage.read_result_image_data(meter_id)
        return data, 200, {'Content-Type': 'image/jpeg'} 
    except FileNotFoundError:
        return 'Meter not found', 404

@app.route('/meter/<identifier:meter_id>/reset', methods=['GET'])
def reset_meter(meter_id):
    value = request.args.get('value', default=None, type=float)
    storage.remove(meter_id)

    if value is not None:
        blank_image = Image.new('RGB', (1, 1))
        storage.store(meter_id, value, blank_image, blank_image)

    return 'Meter reset', 200

def __request_image():
    image_data = request.get_data()

    # if 'base64' in image_data.decode('utf-8'):
        # image_data = image_data.decode('utf-8').split('base64,')[1]
        # image_data = base64.b64decode(image_data)

    return Image.open(BytesIO(image_data))
