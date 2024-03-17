from PIL import Image
from src.digitizer import Digitizer

model_file = 'models/yolov8-detect-20240229.onnx'
image_file = 'samples/watermeter1.jpg'

image = Image.open(image_file)
reading, _ = Digitizer(model_file).detect(image)

print(reading)
