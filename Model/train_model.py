"""Train the Decision Tree traffic-priority classifier."""
from pathlib import Path
import joblib,numpy as np,pandas as pd
from sklearn.metrics import accuracy_score,classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
ROOT=Path(__file__).resolve().parents[1];DATA_PATH=ROOT/"Data"/"traffic_dataset.csv";MODEL_PATH=ROOT/"Model"/"model.pkl";ENCODER_PATH=ROOT/"Model"/"label_encoders.pkl"
CATEGORICAL=("TimeOfDay","Weather","Emergency","TrafficDensity","CongestionLevel","BestRoad")

def _demo_data(n=4000):
    rng=np.random.default_rng(42);roads=np.array(["North","South","East","West"]);rows=[]
    for _ in range(n):
        v=rng.integers(0,55,4);w=rng.integers(0,120,4);score=v*5+w*2;em=rng.choice(["None","North","South","East","West"],p=[.8,.05,.05,.05,.05]);
        if em!="None":score[dict(zip(roads,range(4)))[em]]+=1000
        best=roads[int(np.argmax(score))];total=int(v.sum());density="Low" if total<=45 else "Medium" if total<=100 else "High" if total<=150 else "Very High";wait=float(w.max());cong="Low" if wait<35 and v.max()<15 else "Medium" if wait<70 and v.max()<30 else "High" if wait<100 and v.max()<45 else "Very High";rows.append([*v,*w,rng.choice(["Morning","Afternoon","Evening","Night"]),rng.choice(["Clear","Foggy","Rainy"]),em,density,cong,int(rng.choice([10,20,30,40,50])),best])
    return pd.DataFrame(rows,columns=["NorthVehicles","SouthVehicles","EastVehicles","WestVehicles","NorthWaitingTime","SouthWaitingTime","EastWaitingTime","WestWaitingTime","TimeOfDay","Weather","Emergency","TrafficDensity","CongestionLevel","GreenSignalTime","BestRoad"])

def train():
    df=pd.read_csv(DATA_PATH,keep_default_na=False) if DATA_PATH.exists() else _demo_data()
    encoders={}
    for col in CATEGORICAL:enc=LabelEncoder();df[col]=enc.fit_transform(df[col].astype(str));encoders[col]=enc
    X=df.drop(columns="BestRoad");y=df["BestRoad"];X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.20,random_state=42,stratify=y)
    model=DecisionTreeClassifier(max_depth=15,random_state=42);model.fit(X_train,y_train);pred=model.predict(X_test);acc=accuracy_score(y_test,pred);MODEL_PATH.parent.mkdir(parents=True,exist_ok=True);joblib.dump(model,MODEL_PATH);joblib.dump(encoders,ENCODER_PATH)
    print(f"Records: {len(df)} | Train: {len(X_train)} | Test: {len(X_test)} | Accuracy: {acc*100:.2f}%");print(classification_report(y_test,pred,target_names=encoders["BestRoad"].classes_));return model,encoders,acc
if __name__=="__main__":train()
