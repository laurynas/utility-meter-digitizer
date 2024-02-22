# utility-meter-reader

Digitize utility meter readings from photos

## Demo

> python demo.py

# Server

Start server

> python server.py

POST image using curl

> curl -X POST --data-binary @samples/watermeter1.jpg http://localhost:8000/detect

## Model

Model was trained using [YOLOv8](https://docs.ultralytics.com/tasks/detect/#__tabbed_1_2) open source [utility meters dataset](https://universe.roboflow.com/watermeter-jvlgr/utility-meter-reading-dataset-for-automatic-reading-yolo) from Roboflow.

> yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=100 imgsz=640 device=mps

`device=mps` enables GPU usage on MacBook for faster training.

Converting to onnx format

> yolo export model=best.pt format=onnx

## Credits

- [Utility meters dataset](https://universe.roboflow.com/watermeter-jvlgr/utility-meter-reading-dataset-for-automatic-reading-yolo) from Roboflow
- [ONNX YOLOv8 Object Detection](https://github.com/ibaiGorordo/ONNX-YOLOv8-Object-Detection/) by Ibai Gorordo