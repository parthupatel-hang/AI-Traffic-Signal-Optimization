"""Train the Decision Tree traffic-priority classifier."""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.metrics import accuracy_score,classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

ROOT=Path(__file__).resolve().parents[1];DATA_PATH=ROOT/"Data"/"traffic_dataset.csv";MODEL_PATH=ROOT/"Model"/"model.pkl";ENCODER_PATH=ROOT/"Model"/"label_encoders.pkl"
CATEGORICAL=("TimeOfDay","Weather","Emergency","TrafficDensity","CongestionLevel","BestRoad")

def train():
    df=pd.read_csv(DATA_PATH,keep_default_na=False);encoders={}
    for col in CATEGORICAL:
        enc=LabelEncoder();df[col]=enc.fit_transform(df[col].astype(str));encoders[col]=enc
    X=df.drop(columns="BestRoad");y=df["BestRoad"]
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.20,random_state=42,stratify=y)
    model=DecisionTreeClassifier(max_depth=15,random_state=42);model.fit(X_train,y_train);pred=model.predict(X_test)
    acc=accuracy_score(y_test,pred);joblib.dump(model,MODEL_PATH);joblib.dump(encoders,ENCODER_PATH)
    print(f"Records: {len(df)} | Train: {len(X_train)} | Test: {len(X_test)} | Accuracy: {acc*100:.2f}%")
    print(classification_report(y_test,pred,target_names=encoders["BestRoad"].classes_));return model,encoders,acc

if __name__=="__main__":train()
