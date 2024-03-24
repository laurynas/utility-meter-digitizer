# Utility Meter Digitizer

Digitize utility meter readings from photos using AI model.

Can be used with Home Assistant to digitize utility meter readings from camera. [Integration component](https://github.com/laurynas/hass-utility-meter-digitizer).

This project is inspired by [AI on the Edge device project](https://github.com/jomjol/AI-on-the-edge-device), but the goal is a bit different:

1. Take picture from any camera (even the cheapest ESP32CAM).
2. No need for preselecting number positions or aligning - AI model detects automatically.

![result](samples/watermeter2_result.jpg)

## Demo

```shell
python demo.py
```

# Server

Start server

```shell
gunicorn app:app
```

POST image using curl

```shell
curl -X POST --data-binary @samples/watermeter1.jpg http://localhost:8000/digitize
```

## Docker

You can start the server on Docker like this:
```shell
docker run -p 8000:8000 kurmisrainas/utility-meter-digitizer
```
Also you can use docker-compose:

```yaml
services:
  utility-meter-digitizer:
    image: kurmisrainas/utility-meter-digitizer
    ports:
      - 8000:8000
```

## Model

Model was trained using [YOLOv8](https://docs.ultralytics.com/tasks/detect/#__tabbed_1_2) open source [utility meters dataset](https://universe.roboflow.com/watermeter-jvlgr/utility-meter-reading-dataset-for-automatic-reading-yolo/dataset/1) from Roboflow.

```shell
yolo task=detect mode=train model=yolov8n.pt data=data.yaml epochs=100 imgsz=640 device=mps
```

`device=mps` enables GPU usage on MacBook for faster training.

Converting to onnx format

```shell
yolo export model=best.pt format=onnx
```

## Credits

- [Utility meters dataset](https://universe.roboflow.com/watermeter-jvlgr/utility-meter-reading-dataset-for-automatic-reading-yolo/dataset/1) from Roboflow
- [ONNX YOLOv8 Object Detection](https://github.com/ibaiGorordo/ONNX-YOLOv8-Object-Detection/) by Ibai Gorordo
