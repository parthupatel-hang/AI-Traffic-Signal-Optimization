"""Generate a feature-importance chart for the trained Decision Tree."""
from pathlib import Path
import joblib,matplotlib.pyplot as plt,pandas as pd
ROOT=Path(__file__).resolve().parents[1];model=joblib.load(ROOT/"Model"/"model.pkl")
features=list(getattr(model,"feature_names_in_",[]));df=pd.DataFrame({"Feature":features,"Importance":model.feature_importances_}).sort_values("Importance")
plt.figure(figsize=(10,6));plt.barh(df["Feature"],df["Importance"]);plt.xlabel("Importance Score");plt.title("Decision Tree Feature Importance");plt.tight_layout();plt.savefig(ROOT/"Model"/"feature_importance.png",dpi=300,bbox_inches="tight")
print("Saved Model/feature_importance.png")
