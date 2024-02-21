from flask import Flask, request
from PIL import Image
from src.digitizer import Digitizer

MODEL_FILE = 'models/yolov8-detect-20240220.pt'
PORT = 8000

app = Flask(__name__)
digitizer = Digitizer(MODEL_FILE)

@app.route('/detect', methods=['POST'])
def detect():
    image = Image.open(request.files['image'])
    result = digitizer.detect(image)
    return result

app.run(port=PORT)