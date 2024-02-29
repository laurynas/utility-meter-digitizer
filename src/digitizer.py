from .yolov8 import YOLOv8

class Digitizer:
    CLASSES = range(0, 10)
    DEFAULT_THRESHOLD = 0.7

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

        results = self.remove_overlapping(results)

        return results

    # remove overlapping boxes by x coordinate keeping the one with the highest score
    def remove_overlapping(self, results):
        if len(results) == 0:
            return []

        output = [results[0]]

        for i in range(1, len(results)):
            if results[i][2][0] > output[-1][2][2]:
                output.append(results[i])
            elif results[i][1] > output[-1][1]:
                output[-1] = results[i]

        return output