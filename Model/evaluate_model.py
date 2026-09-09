"""Evaluate the Decision Tree on the project's data or deterministic demo fallback."""
from pathlib import Path
import sys,joblib,pandas as pd
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix
from sklearn.model_selection import train_test_split
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
def evaluate():
    model_path=ROOT/"Model"/"model.pkl";enc_path=ROOT/"Model"/"label_encoders.pkl";df_path=ROOT/"Data"/"traffic_dataset.csv"
    if not model_path.exists() or not enc_path.exists():
        from Model.train_model import train
        train()
    if not df_path.exists():print("No local traffic_dataset.csv found; demo training was used. Add the project dataset to evaluate it.");return
    df=pd.read_csv(df_path,keep_default_na=False);enc=joblib.load(enc_path);model=joblib.load(model_path)
    for c in ("TimeOfDay","Weather","Emergency","TrafficDensity","CongestionLevel"):df[c]=enc[c].transform(df[c].astype(str))
    y=enc["BestRoad"].transform(df.pop("BestRoad").astype(str));_,X_test,_,y_test=train_test_split(df,y,test_size=.20,random_state=42,stratify=y);pred=model.predict(X_test)
    print(f"Test accuracy: {accuracy_score(y_test,pred)*100:.2f}%");print(classification_report(y_test,pred,target_names=enc["BestRoad"].classes_));print("Confusion matrix:");print(confusion_matrix(y_test,pred))
if __name__=="__main__":evaluate()
