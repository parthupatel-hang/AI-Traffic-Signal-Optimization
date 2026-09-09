# AI Traffic Signal Optimization

An AI-powered intelligent traffic management system that uses a Decision Tree machine learning model to optimize traffic signal timing at a four-way intersection.

## Overview

The system analyzes traffic conditions such as:

- Vehicle count on each road
- Waiting time
- Traffic density
- Congestion level
- Weather conditions
- Time of day
- Emergency vehicle presence

Based on these inputs, the system predicts which road should receive the green signal to improve traffic flow and reduce congestion.

## Project Phases

### Phase 1 — Decision Tree Model + Simulation GUI
- Train a Decision Tree classifier from traffic data.
- Save and load the trained model.
- Visualize the decision tree and feature importance.
- Run a four-way intersection simulation through a Tkinter GUI.

### Phase 2 — Adaptive Traffic Optimization
- Adapt signal priority according to changing traffic conditions.
- Use traffic counts and congestion-related inputs to dynamically determine the next green signal.
- Support real-time-style traffic simulation and AI-assisted decision making.

## Technology Stack

- Python
- Scikit-learn
- Pandas
- NumPy
- Tkinter
- Matplotlib
- Graphviz
- Joblib
- YOLO-based vehicle detection components

## Project Structure

```text
AI-Traffic-Signal-Optimization/
├── Data/
│   └── traffic_dataset.csv
├── GUI/
│   ├── ai_controller.py
│   ├── app.py
│   ├── intersection.py
│   ├── launcher.py
│   ├── traffic_lights.py
│   └── vehicles.py
├── Input/
│   ├── config/
│   │   └── road_config.json
│   └── images/
├── Model/
│   ├── decision_tree_model.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   ├── visualize_tree.py
│   └── feature_importance.py
├── Output/
│   ├── detections/
│   ├── reports/
│   └── videos/
├── requirements.txt
└── README.md
```

## Ahmedabad Junction Mode

The simulation is designed around a realistic four-way junction layout and can be configured for the Ahmedabad/Gujarat traffic scenario.

Signal orientation:

- North traffic signal → South side
- South traffic signal → North side
- East traffic signal → West side
- West traffic signal → East side

The intended logic supports one active green direction at a time, stop-line behavior, and adaptive signal selection.

## Installation

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Running the GUI

From the project root:

```bash
python GUI/app.py
```

## Model Training

Train the Decision Tree model using the project training script:

```bash
python Model/train_model.py
```

## Notes

Large model files and local virtual-environment files should not be committed unnecessarily. The repository should contain source code, datasets/configuration required for reproducibility, documentation, and lightweight generated artifacts.

## Author

**Parth Patel**  
Integrated B.Sc. – M.Sc. IT (Cyber Security & Digital Forensics)
