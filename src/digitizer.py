from .yolov8 import YOLOv8

class Digitizer:
    CLASSES = range(0, 10)
    DEFAULT_THRESHOLD = 0.7

    def __init__(self, model_file):
        self.model = YOLOv8(model_file)

    def detect(self, image, conf_threshold=DEFAULT_THRESHOLD):
        boxes, scores, class_ids = self.model.detect_objects(image, conf_threshold)

        results = zip(class_ids, scores, boxes)

        # select only the classes we are interested in
        results = [r for r in results if r[0] in self.CLASSES]

        # sort by x coordinate
        results = sorted(results, key=lambda b: b[2][0])
        results = self._remove_overlapping(results)
        reading = self._build_string(results)

        return reading, results

    # remove overlapping boxes by x coordinate keeping the one with the highest score
    def _remove_overlapping(self, results):
        if len(results) == 0:
            return []

        output = [results[0]]

        for i in range(1, len(results)):
            if results[i][2][0] > output[-1][2][2]:
                output.append(results[i])
            elif results[i][1] > output[-1][1]:
                output[-1] = results[i]

        return output

    def _build_string(self, results):
        return ''.join([str(int(result[0])) for result in results])