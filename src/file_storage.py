import json
import os

class FileStorage:
    def __init__(self, path):
        self.path = path

    def store(self, meter_id, value, image, result_image):
        self._write_data(f'{meter_id}.json', {'value': value})
        self._write_image(f'{meter_id}.jpg', image)
        self._write_image(f'{meter_id}_result.jpg', result_image)
        
    def read_value(self, meter_id):
        return self._read_data(f'{meter_id}.json')['value']

    def read_image_data(self, meter_id):
        return self._read_image_data(f'{meter_id}.jpg')

    def read_result_image_data(self, meter_id):
        return self._read_image_data(f'{meter_id}_result.jpg')

    def remove(self, meter_id):
        files = [f'{meter_id}.json', f'{meter_id}.jpg', f'{meter_id}_result.jpg']
        for file in files:
            path = os.path.join(self.path, file)
            if os.path.exists(path):
                os.remove(path)
        
    def _write_data(self, name, data):
        with open(os.path.join(self.path, name), 'w') as f:
            json.dump(data, f)

    def _read_data(self, name):
        with open(os.path.join(self.path, name), 'r') as f:
            return json.load(f)

    def _write_image(self, name, image):
        with open(os.path.join(self.path, name), 'wb') as f:
            image.save(f, 'JPEG')

    def _read_image_data(self, name):
        return open(os.path.join(self.path, name), 'rb').read()
