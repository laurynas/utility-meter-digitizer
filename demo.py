from lib.digitizer import Digitizer

MODEL_FILE = 'models/yolov8-detect-20240220.pt'
IMAGE_FILE = 'samples/watermeter1.jpg'

result = Digitizer(MODEL_FILE).run(IMAGE_FILE)

print(result)
