"""Reusable wrapper around the trained traffic Decision Tree model."""
from pathlib import Path
import joblib
import pandas as pd

class DecisionTreeTrafficModel:
    def __init__(self,model_path=None,encoder_path=None):
        root=Path(__file__).resolve().parent;self.model_path=Path(model_path or root/"model.pkl");self.encoder_path=Path(encoder_path or root/"label_encoders.pkl")
        self.model=joblib.load(self.model_path);self.encoders=joblib.load(self.encoder_path)
    def predict(self,features):
        row=dict(features)
        for column in ("TimeOfDay","Weather","Emergency","TrafficDensity","CongestionLevel"):
            enc=self.encoders[column];value=str(row[column]);value=value if value in enc.classes_ else ("None" if "None" in enc.classes_ else enc.classes_[0]);row[column]=int(enc.transform([value])[0])
        frame=pd.DataFrame([row]);pred=int(self.model.predict(frame)[0]);road=str(self.encoders["BestRoad"].inverse_transform([pred])[0]);conf=float(max(self.model.predict_proba(frame)[0])*100) if hasattr(self.model,"predict_proba") else 0.0
        return road,conf
