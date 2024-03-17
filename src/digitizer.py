from .yolov8 import YOLOv8
from .detected_object import DetectedObject

class Digitizer:
    CLASSES = range(0, 10)
    DEFAULT_THRESHOLD = 0.7

    def __init__(self, model_file):
        self.model = YOLOv8(model_file)

    def detect(self, image, conf_threshold=DEFAULT_THRESHOLD):
        output = self.model.detect_objects(image, conf_threshold)

        results = [DetectedObject(*r) for r in zip(*output)]
        # select only the classes we are interested in
        results = [r for r in results if r.class_id in self.CLASSES]
        # sort by x coordinate
        results = sorted(results, key=lambda r: r.box[0])
        results = self._remove_overlapping(results)

        reading = ''.join([str(r.class_id) for r in results])

        return reading, results

    # remove overlapping boxes by x coordinate keeping the one with the highest score
    def _remove_overlapping(self, results):
        if len(results) == 0:
            return []

        output = [results[0]]

        for i in range(1, len(results)):
            if results[i].box[0] > output[-1].box[2]:
                output.append(results[i])
            elif results[i].score > output[-1].score:
                output[-1] = results[i]

        return output