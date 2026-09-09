"""Bridge between GUI traffic features and the trained Decision Tree model."""
from pathlib import Path
import joblib,numpy as np,pandas as pd
FEATURE_COLUMNS=["NorthVehicles","SouthVehicles","EastVehicles","WestVehicles","NorthWaitingTime","SouthWaitingTime","EastWaitingTime","WestWaitingTime","TimeOfDay","Weather","Emergency","TrafficDensity","CongestionLevel","GreenSignalTime"]
CATEGORICAL_COLUMNS=["TimeOfDay","Weather","Emergency","TrafficDensity","CongestionLevel"]
class AIController:
    def __init__(self,model_path=None,encoder_path=None):
        root=Path(__file__).resolve().parents[1];self.model_path=Path(model_path or root/"Model"/"model.pkl");self.encoder_path=Path(encoder_path or root/"Model"/"label_encoders.pkl")
        if not self.model_path.exists() or not self.encoder_path.exists():
            from Model.train_model import train
            train()
        self.model=joblib.load(self.model_path);self.label_encoders=joblib.load(self.encoder_path);self.last_prediction,self.last_confidence,self.last_features="--",0.0,{}
    def _safe_encode(self,column,value):
        enc=self.label_encoders[column];value=str(value)
        if value not in enc.classes_:value="None" if "None" in enc.classes_ else enc.classes_[0]
        return int(enc.transform([value])[0])
    def build_model_input(self,features):
        row={k:features[k] for k in FEATURE_COLUMNS if k not in CATEGORICAL_COLUMNS}
        for c in CATEGORICAL_COLUMNS:row[c]=self._safe_encode(c,features[c])
        return pd.DataFrame([row],columns=FEATURE_COLUMNS)
    def predict_best_road(self,features):
        sample=self.build_model_input(features);prediction=int(self.model.predict(sample)[0]);target=self.label_encoders["BestRoad"];road=str(target.inverse_transform([prediction])[0]);confidence=float(np.max(self.model.predict_proba(sample))*100) if hasattr(self.model,"predict_proba") else 0.0;self.last_prediction,self.last_confidence,self.last_features=road,confidence,features.copy();return road,confidence
