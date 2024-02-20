from flask import Flask, request
from PIL import Image
from lib.digitizer import Digitizer

MODEL_FILE = 'models/yolov8-detect-20240220.pt'
PORT = 8000

app = Flask(__name__)
digitizer = Digitizer(MODEL_FILE)

@app.route('/detect', methods=['POST'])
def detect():
    image = Image.open(request.files['image'])
    result = digitizer.run(image)
    return result

if __name__ == '__main__':
    app.run(port=PORT)