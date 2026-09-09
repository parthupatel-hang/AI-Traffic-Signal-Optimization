"""Assign vehicle centroids to calibrated road-of-interest polygons."""
import json
from pathlib import Path
import cv2,numpy as np

class RoadAssigner:
    def __init__(self,config_path):
        with open(config_path,encoding="utf-8") as f:cfg=json.load(f)
        self.width=int(cfg["image_width"]);self.height=int(cfg["image_height"])
        self.polygons={r:np.array([[round(x*self.width),round(y*self.height)] for x,y in d["polygon"]],dtype=np.int32) for r,d in cfg["roads"].items()}
    def assign(self,x,y):
        hits=[r for r,p in self.polygons.items() if cv2.pointPolygonTest(p,(float(x),float(y)),False)>=0]
        if len(hits)==1:return hits[0]
        if not hits:return "UNASSIGNED"
        point=np.array([x,y],dtype=float);return min(hits,key=lambda r:np.sum((self.polygons[r].mean(axis=0)-point)**2))
    def assign_detection(self,detection):
        item=dict(detection);x,y=item.get("center",((item["bbox"][0]+item["bbox"][2])/2,(item["bbox"][1]+item["bbox"][3])/2));item["road"]=self.assign(x,y);return item
