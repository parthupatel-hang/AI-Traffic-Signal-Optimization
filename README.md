# AI Traffic Signal Optimization Using Decision Tree Model

An intelligent four-way traffic management system that combines a **Decision Tree classifier**, adaptive signal-control logic, and **YOLOv8 vehicle detection** to prioritize traffic movement.

## Key Features

- Decision Tree prediction of the road that should receive priority.
- Adaptive signal switching based on vehicle count and waiting time.
- Minimum/maximum green-time control with yellow and all-red clearance.
- Emergency-vehicle priority in the simulation.
- Per-road queue and waiting-time monitoring.
- YOLOv8 detection for cars, motorcycles, buses, and trucks.
- Persistent vehicle IDs through centroid tracking.
- Configurable road-of-interest polygons.
- Separate YOLO image/video analysis window.
- Ahmedabad/Gujarat-oriented four-road intersection layout.

## Architecture

```text
Traffic Simulation GUI
        │
        ├── Vehicle Manager
        ├── Signal Controller
        └── Decision Tree AI Controller
                │
                ├── vehicle counts
                ├── waiting times
                ├── time of day
                ├── weather
                ├── emergency state
                └── traffic/congestion levels

YOLOv8 Vision Pipeline
        │
        ├── Vehicle Detection
        ├── Centroid Tracking
        ├── Road Assignment (ROI)
        ├── Traffic Metrics
        └── Adaptive Signal Recommendation
```

## Repository Structure

```text
AI-Traffic-Signal-Optimization/
├── Data/
│   └── traffic_dataset.csv
├── GUI/
│   ├── __init__.py
│   ├── ai_controller.py
│   ├── app.py
│   ├── intersection.py
│   ├── traffic_lights.py
│   └── vehicles.py
├── Input/
│   ├── config/
│   │   └── road_config.json
│   └── images/
│       └── traffic_test.jpg
├── Model/
│   ├── model.pkl
│   ├── label_encoders.pkl
│   ├── decision_tree_model.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   ├── feature_importance.py
│   ├── visualize_tree.py
│   ├── decision_tree.png
│   └── feature_importance.png
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
├── tests/
│   └── test_core.py
├── .gitignore
├── requirements.txt
├── INSTALL.bat
├── DOWNLOAD_MODEL.bat
├── RUN_PHASE2.bat
└── README.md
```

## Ahmedabad Junction Mode

The simulation follows the intended four-road orientation:

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

Or install manually:

```bash
python -m venv venv
venv\\Scripts\\activate
python -m pip install -r requirements.txt
python -m Model.train_model
```

The YOLOv8s weight file is intentionally **not stored in the repository**. Ultralytics downloads it automatically when the detector is first initialized. `DOWNLOAD_MODEL.bat` can also be used to prepare it locally.

## Run the Main GUI

From the repository root:

```bash
python GUI/app.py
```

Or on Windows:

```bat
RUN_PHASE2.bat
```

## Train / Evaluate the Decision Tree

```bash
python Model/train_model.py
python Model/evaluate_model.py
```

The training script uses an 80/20 stratified split and a Decision Tree with `max_depth=15` and `random_state=42`. The dataset contains 20,000 records and 14 model input features plus the `BestRoad` target.

Generate model visualizations with:

```bash
python Model/feature_importance.py
python Model/visualize_tree.py
```

## YOLO Vision

The main GUI contains a separate **YOLO Detection** window for image/video analysis. The vision pipeline also supports:

- YOLOv8 vehicle detection
- centroid-based tracking
- calibrated road assignment
- queue length and waiting-time metrics
- adaptive green-road recommendation

ROI calibration can be run with:

```bash
python Vision/calibration.py
```

## Testing

Run the smoke tests with:

```bash
python -m pytest tests
```

The tests cover dataset schema, model prediction, ROI assignment, and tracker ID persistence.

## Generated Files

Runtime detection images, reports, videos, Python caches, virtual environments, and local YOLO weights are intentionally excluded from Git. This keeps the repository source-focused and reproducible.

## Technology Stack

Python · Tkinter · Scikit-learn · Pandas · NumPy · Joblib · Matplotlib · OpenCV · Pillow · Ultralytics YOLOv8

## Author

**Parth Patel**  
Integrated B.Sc. – M.Sc. IT (Cyber Security & Digital Forensics)
