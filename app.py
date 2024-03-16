import os
from PIL import Image
from src.digitizer import Digitizer
from io import BytesIO
from flask import Flask, request

MODEL_FILE = 'models/yolov8-detect-20240229.onnx'

digitizer = Digitizer(MODEL_FILE)
app = Flask(__name__)

@app.route('/digitize', methods=['POST'])
def digitize():
    data = request.get_data()
    image = Image.open(BytesIO(data))
    result = digitizer.detect_string(image)
    return result
