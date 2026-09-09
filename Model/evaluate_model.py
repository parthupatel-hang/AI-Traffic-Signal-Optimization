"""Evaluate the bundled Decision Tree on a stratified 80/20 split."""
from pathlib import Path
import joblib,pandas as pd
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
ROOT=Path(__file__).resolve().parents[1]
def evaluate():
    df=pd.read_csv(ROOT/"Data"/"traffic_dataset.csv",keep_default_na=False);enc=joblib.load(ROOT/"Model"/"label_encoders.pkl");model=joblib.load(ROOT/"Model"/"model.pkl")
    for c in ("TimeOfDay","Weather","Emergency","TrafficDensity","CongestionLevel"):df[c]=enc[c].transform(df[c].astype(str))
    y=enc["BestRoad"].transform(df.pop("BestRoad").astype(str));_,X_test,_,y_test=train_test_split(df,y,test_size=.20,random_state=42,stratify=y)
    pred=model.predict(X_test);print(f"Test accuracy: {accuracy_score(y_test,pred)*100:.2f}%");print(classification_report(y_test,pred,target_names=enc["BestRoad"].classes_));print("Confusion matrix:");print(confusion_matrix(y_test,pred))
if __name__=="__main__":evaluate()
