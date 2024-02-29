from .yolov8 import YOLOv8

class Digitizer:
    CLASSES = range(0, 9)
    DEFAULT_THRESHOLD = 0.5

    def __init__(self, model_file):
        self.model = YOLOv8(model_file)

    def detect_string(self, image, conf_threshold=DEFAULT_THRESHOLD):
        results = self.detect(image, conf_threshold)
        reading = ''

        for result in results:
            reading += str(int(result[0]))

        return reading
    
    def detect(self, image, conf_threshold=DEFAULT_THRESHOLD):
        boxes, scores, class_ids = self.model.detect_objects(image, conf_threshold)

        results = zip(class_ids, scores, boxes)

        # filter out digits
        results = [r for r in results if r[0] in self.CLASSES]

        # sort by x coordinate
        results = sorted(results, key=lambda b: b[2][0])

        return results  