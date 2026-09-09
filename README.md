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
│   ├── config/road_config.json
│   └── images/traffic_test.jpg
├── Model/
│   ├── model.pkl
│   ├── label_encoders.pkl
│   ├── decision_tree_model.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   ├── feature_importance.py
│   └── visualize_tree.py
├── Vision/
├── tests/
├── .gitignore
├── requirements.txt
├── INSTALL.bat
├── DOWNLOAD_MODEL.bat
├── RUN_PHASE2.bat
└── README.md
```

## Original Project Data and Model

This repository is intended to reproduce the supplied project directly. The **original 20,000-record `Data/traffic_dataset.csv`** is required by the project and is not replaced by demo or synthetic data. The trained Decision Tree artifacts are `Model/model.pkl` and `Model/label_encoders.pkl`.

Do not run model training unless you intentionally want to regenerate the supplied model artifacts. The normal run uses the bundled model and encoder files.

## Ahmedabad Junction Mode

The simulation follows the intended orientation:

- North signal → South side
- South signal → North side
- East signal → West side
- West signal → East side

Only one direction is green at a time. The simulation includes stop-line behavior, free-left movement, yellow transition, and all-red clearance.

## Installation — Windows

Run:

```bat
INSTALL.bat
```

Manual setup:

```bash
python -m venv venv
venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

The YOLOv8s weights are downloaded automatically by Ultralytics when first required, so the large weight file does not need to be bundled with the source repository.

## Run the Project

From the repository root:

```bash
python GUI/app.py
```

Or on Windows:

```bat
RUN_PHASE2.bat
```

After cloning/downloading the repository, the supplied dataset and Decision Tree artifacts are already available at their project paths, so no separate dataset download is required.

## Train / Evaluate the Decision Tree

Training intentionally requires the original project dataset:

```bash
python Model/train_model.py
```

Evaluate the trained model:

```bash
python Model/evaluate_model.py
```

Generate visualizations:

```bash
python Model/feature_importance.py
python Model/visualize_tree.py
```

Training uses an 80/20 stratified split and a Decision Tree with `max_depth=15` and `random_state=42`.

## YOLO Vision

The separate YOLO window supports traffic image/video analysis. The vision pipeline combines YOLO detection, centroid tracking, calibrated road assignment, queue/waiting metrics, and adaptive green-road recommendation.

ROI calibration:

```bash
python Vision/calibration.py
```

## Testing

```bash
python -m pytest tests
```

## Repository Hygiene

Virtual environments, Python caches, runtime detection outputs, local YOLO weights, and temporary files are excluded from Git. The original project dataset and required Decision Tree artifacts are intentionally treated as project inputs and are kept available for direct reproduction.

## Technology Stack

Python · Tkinter · Scikit-learn · Pandas · NumPy · Joblib · Matplotlib · OpenCV · Pillow · Ultralytics YOLOv8

## Author

**Parth Patel**  
Integrated B.Sc. – M.Sc. IT (Cyber Security & Digital Forensics)
