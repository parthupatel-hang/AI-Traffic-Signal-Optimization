"""Command-line prediction helper."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from GUI.ai_controller import AIController

def predict_best_road(**features):return AIController().predict_best_road(features)

if __name__=="__main__":
    road,confidence=predict_best_road(NorthVehicles=30,SouthVehicles=15,EastVehicles=40,WestVehicles=10,NorthWaitingTime=60,SouthWaitingTime=30,EastWaitingTime=80,WestWaitingTime=20,TimeOfDay="Evening",Weather="Clear",Emergency="None",TrafficDensity="High",CongestionLevel="High",GreenSignalTime=40)
    print(f"Best Road : {road}\nConfidence: {confidence:.2f}%")
