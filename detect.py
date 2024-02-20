from ultralytics import YOLO

MODEL_FILE = 'models/yolov8-detect-20240220.pt'
IMAGE_FILE = 'samples/watermeter1.jpg'
CONFIDENCE = 0.5

model = YOLO(MODEL_FILE)
results = model(IMAGE_FILE, conf=CONFIDENCE)
result = results[0]

#result.show()

print(result.tojson())