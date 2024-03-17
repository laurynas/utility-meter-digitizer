from .yolov8 import YOLOv8
from .detected_object import DetectedObject

class Digitizer:
    CLASSES = range(0, 10)
    DEFAULT_THRESHOLD = 0.7

    def __init__(self, model_file):
        self.model = YOLOv8(model_file)

    def detect(self, image, decimals=0, conf_threshold=DEFAULT_THRESHOLD):
        output = self.model.detect_objects(image, conf_threshold)

        objects = [DetectedObject(*r) for r in zip(*output)]
        # select only the classes we are interested in
        objects = [o for o in objects if o.class_id in self.CLASSES]
        # sort by x coordinate
        objects = sorted(objects, key=lambda o: o.box[0])
        objects = self._remove_overlapping(objects)

        value = self._digitize(objects, decimals)

        return value, objects

    # remove overlapping boxes by x coordinate keeping the one with the highest score
    def _remove_overlapping(self, objects):
        if len(objects) == 0:
            return []

        output = [objects[0]]

        for i in range(1, len(objects)):
            if objects[i].box[0] > output[-1].box[2]:
                output.append(objects[i])
            elif objects[i].score > output[-1].score:
                output[-1] = objects[i]

        return output

    def _digitize(self, objects, decimals):
        string = ''.join([str(o.class_id) for o in objects])

        if len(string) > 0:
            return float(string) / (10 ** decimals)
        else:
            return None
