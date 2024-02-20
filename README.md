# utility-meter-reader

Digitize utility meter readings from photos

## Model

Model was trained using YOLOv8 open source [utility meters dataset](https://universe.roboflow.com/watermeter-jvlgr/utility-meter-reading-dataset-for-automatic-reading-yolo) from Roboflow.

> yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=100 imgsz=640 device=mps

`device=mps` enables GPU usage on MacBook for faster training.
