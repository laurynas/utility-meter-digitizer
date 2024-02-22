from PIL import Image
from src.digitizer import Digitizer

model_file = 'models/yolov8-detect-20240220.onnx'
image_file = 'samples/watermeter1.jpg'

image = Image.open(image_file)
result = Digitizer(model_file).detect_string(image)

print(result)
