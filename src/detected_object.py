class DetectedObject:
    def __init__(self, box, score, class_id):
        self.box = box
        self.score = score
        self.class_id = class_id