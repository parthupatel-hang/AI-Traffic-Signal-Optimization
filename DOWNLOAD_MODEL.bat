@echo off
setlocal
cd /d "%~dp0"
call venv\Scripts\activate.bat 2>nul
python -c "from ultralytics import YOLO;YOLO('yolov8s.pt');print('YOLOv8s weights are ready.')"
pause
