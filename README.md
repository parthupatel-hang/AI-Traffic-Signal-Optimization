# AI Traffic Signal Optimization Using Decision Tree Model

An intelligent four-way traffic management system combining a **Decision Tree classifier**, adaptive signal-control logic, and **YOLOv8 vehicle detection**.

## Key Features

- Decision Tree prediction of the road that should receive priority.
- Adaptive signal switching using vehicle count and waiting time.
- Minimum/maximum green timing with yellow and all-red clearance.
- Emergency-vehicle priority in the simulation.
- Per-road queue and waiting-time monitoring.
- YOLOv8 detection for cars, motorcycles, buses, and trucks.
- Persistent vehicle IDs through centroid tracking.
- Configurable road-of-interest polygons.
- Separate YOLO image/video analysis window.
- Ahmedabad/Gujarat-oriented four-way junction layout.

## Architecture

```text
Traffic Simulation GUI
  ├── Vehicle Manager
  ├── Signal Controller
  └── Decision Tree AI Controller

YOLOv8 Vision Pipeline
  ├── Vehicle Detection
  ├── Centroid Tracking
  ├── Road Assignment / ROI
  ├── Traffic Metrics
  └── Adaptive Green Recommendation
```

## Repository Structure

```text
AI-Traffic-Signal-Optimization/
├── Data/
│   └── README.md
├── GUI/
│   ├── __init__.py
│   ├── ai_controller.py
│   ├── app.py
│   ├── intersection.py
│   ├── traffic_lights.py
│   └── vehicles.py
├── Input/config/
│   └── road_config.json
├── Model/
│   ├── README.md
│   ├── __init__.py
│   ├── decision_tree_model.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   ├── feature_importance.py
│   └── visualize_tree.py
├── Vision/
│   ├── __init__.py
│   ├── yolo_detector.py
│   ├── yolo_ui.py
│   ├── tracker.py
│   ├── road_assigner.py
│   ├── traffic_metrics.py
│   ├── adaptive_controller.py
│   ├── pipeline.py
│   ├── video_runner.py
│   └── calibration.py
├── tests/test_core.py
├── .gitignore
├── requirements.txt
├── INSTALL.bat
├── DOWNLOAD_MODEL.bat
├── RUN_PHASE2.bat
└── README.md
```

## Ahmedabad Junction Mode

The simulation follows the intended orientation:

- North signal → South side
- South signal → North side
- East signal → West side
- West signal → East side

Only one direction is green at a time. The simulation includes stop-line behavior, free-left movement, yellow transition, and all-red clearance.

## Installation

### Windows

Run:

```bat
INSTALL.bat
```

Manual setup:

```bash
python -m venv venv
venv\\Scripts\\activate
python -m pip install -r requirements.txt
python -m Model.train_model
```

The YOLOv8s weight file is intentionally not committed. Ultralytics downloads it automatically when the detector is first initialized.

The original 20,000-record traffic dataset is also kept outside the public source tree. If `Data/traffic_dataset.csv` is available locally, training uses it. Otherwise, `train_model.py` creates deterministic demo data so the project remains runnable.

## Run the GUI

```bash
python GUI/app.py
```

or:

```bat
RUN_PHASE2.bat
```

## Train and Evaluate

```bash
python Model/train_model.py
python Model/evaluate_model.py
python Model/feature_importance.py
python Model/visualize_tree.py
```

Training uses an 80/20 stratified split and a Decision Tree with `max_depth=15` and `random_state=42`.

## YOLO Vision

The separate YOLO window supports traffic image/video analysis. The reusable vision pipeline combines YOLO detection, centroid tracking, calibrated road assignment, queue/waiting metrics, and adaptive green-road recommendation.

ROI calibration:

```bash
python Vision/calibration.py
```

## Testing

```bash
python -m pytest tests
```

## Repository Hygiene

Virtual environments, Python caches, runtime detection outputs, local YOLO weights, and generated model binaries are excluded from Git. This keeps the public repository focused on reproducible source code and configuration.

## Technology Stack

Python · Tkinter · Scikit-learn · Pandas · NumPy · Joblib · Matplotlib · OpenCV · Pillow · Ultralytics YOLOv8

## Author

**Parth Patel**  
Integrated B.Sc. – M.Sc. IT (Cyber Security & Digital Forensics)
