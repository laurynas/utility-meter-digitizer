from ultralytics import YOLO

class Digitizer:
    CLASSES = range(0, 9)
    DEFAULT_CONFIDENCE = 0.5

    def __init__(self, model_file):
        self.model = YOLO(model_file)

    def detect(self, image, confidence=DEFAULT_CONFIDENCE):
        rows = self.yolo(image, confidence)

        # sort by x position
        rows = sorted(rows, key=lambda r: r[0])
        reading = ''

        for row in rows:
            reading += str(int(row[-1]))

        return reading
    
    def yolo(self, image, confidence):
        results = self.model(image, conf=confidence, classes=self.CLASSES)
        result = results[0]

        #result.show()
        #print(result.tojson())

        return result.boxes.data.cpu().tolist()