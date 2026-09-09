"""Smoke tests for the core model and vision components."""
from pathlib import Path
import sys
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from GUI.ai_controller import AIController
from Vision.road_assigner import RoadAssigner
from Vision.tracker import CentroidTracker

def test_dataset_schema():
    data=pd.read_csv(ROOT/"Data"/"traffic_dataset.csv",keep_default_na=False)
    assert len(data)>0 and "BestRoad" in data.columns
    assert set(data["BestRoad"].unique())=={"East","North","South","West"}

def test_model_prediction():
    road,confidence=AIController().predict_best_road({"NorthVehicles":10,"SouthVehicles":15,"EastVehicles":35,"WestVehicles":8,"NorthWaitingTime":20,"SouthWaitingTime":40,"EastWaitingTime":90,"WestWaitingTime":15,"TimeOfDay":"Evening","Weather":"Clear","Emergency":"None","TrafficDensity":"High","CongestionLevel":"High","GreenSignalTime":30})
    assert road in {"East","North","South","West"} and 0<=confidence<=100

def test_road_assignment():
    assigner=RoadAssigner(ROOT/"Input"/"config"/"road_config.json")
    assert assigner.assign(960,200)=="NORTH"

def test_tracker_persists_id():
    tracker=CentroidTracker();a=tracker.update([{"bbox":[100,100,140,140],"class_name":"car"}],1.0);b=tracker.update([{"bbox":[105,100,145,140],"class_name":"car"}],1.1)
    assert a[0]["track_id"]==b[0]["track_id"] and b[0]["speed_px_s"]>0
