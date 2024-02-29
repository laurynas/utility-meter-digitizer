from PIL import Image
from src.digitizer import Digitizer
from io import BytesIO
import http.server
import socketserver
import signal

MODEL_FILE = 'models/yolov8-detect-20240229.onnx'
PORT = 8000

digitizer = Digitizer(MODEL_FILE)

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(length)

        image = Image.open(BytesIO(post_data))
        result = digitizer.detect_string(image)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        self.wfile.write(result.encode('utf-8'))
        return

server = socketserver.TCPServer(("", PORT), HTTPRequestHandler)

def signal_handler(sig, frame):
    print('Stopping...')
    server.server_close()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

print(f"Starting server on port {PORT}")
server.serve_forever()