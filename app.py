import os
from PIL import Image
from src.digitizer import Digitizer
from src.route_converters import IdentifierConverter
from io import BytesIO
from flask import Flask, request

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
    data = request.get_data()
    image = Image.open(BytesIO(data))
    image.save(os.path.join(data_dir, f'{meter_id}.jpg'))
    return digitizer.detect_string(image)

@app.route('/meter/<identifier:meter_id>/image', methods=['GET'])
def meter_image(meter_id):
    image_path = os.path.join(data_dir, f'{meter_id}.jpg')
    if not os.path.exists(image_path):
        return 'Image not found', 404
    return open(image_path, 'rb').read(), 200, {'Content-Type': 'image/jpeg'}
