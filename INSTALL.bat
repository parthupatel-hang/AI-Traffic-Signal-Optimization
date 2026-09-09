@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (py -3.10 -m venv venv) else (python -m venv venv)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m Model.train_model
python -c "import torch,cv2,ultralytics,sklearn,pandas,numpy;print('Dependencies: OK');print('PyTorch:',torch.__version__);print('CUDA available:',torch.cuda.is_available())"
python -c "from ultralytics import YOLO;YOLO('yolov8s.pt');print('YOLOv8s: READY')"
echo Installation complete.
pause
