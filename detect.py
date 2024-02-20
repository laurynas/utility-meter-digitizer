from ultralytics import YOLO

MODEL_FILE = 'models/yolov8-detect-20240220.pt'
IMAGE_FILE = 'samples/watermeter1.jpg'
CONFIDENCE = 0.5
CLASSES = range(0, 9)

model = YOLO(MODEL_FILE)
results = model(IMAGE_FILE, conf=CONFIDENCE, classes=CLASSES)
result = results[0]

def digitize(rows):
    # sort by x position
    rows = sorted(rows, key=lambda x: x[0])
    reading = ''

    for row in rows:
        reading += str(int(row[-1]))

    return reading

data = result.boxes.data.cpu().tolist()

print(digitize(data))
#result.show()
#print(result.tojson())
