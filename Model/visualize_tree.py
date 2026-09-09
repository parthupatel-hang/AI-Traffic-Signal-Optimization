"""Export a readable visualization of the trained Decision Tree."""
from pathlib import Path
import joblib,matplotlib.pyplot as plt
from sklearn.tree import plot_tree
ROOT=Path(__file__).resolve().parents[1];model=joblib.load(ROOT/"Model"/"model.pkl");enc=joblib.load(ROOT/"Model"/"label_encoders.pkl")
plt.figure(figsize=(22,12));plot_tree(model,feature_names=list(model.feature_names_in_),class_names=[str(x) for x in enc["BestRoad"].classes_],filled=False,max_depth=5,fontsize=7);plt.tight_layout();plt.savefig(ROOT/"Model"/"decision_tree.png",dpi=220,bbox_inches="tight")
print("Saved Model/decision_tree.png")
