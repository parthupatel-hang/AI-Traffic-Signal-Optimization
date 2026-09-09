"""Interactive ROI calibration utility for Input/config/road_config.json."""
from pathlib import Path
import cv2,json
ROOT=Path(__file__).resolve().parents[1];IMAGE=ROOT/"Input"/"images"/"traffic_test.jpg";CONFIG=ROOT/"Input"/"config"/"road_config.json"

def calibrate():
    image=cv2.imread(str(IMAGE))
    if image is None:raise SystemExit(f"Missing calibration image: {IMAGE}")
    with open(CONFIG,encoding="utf-8") as f:cfg=json.load(f)
    roads=("NORTH","SOUTH","EAST","WEST");points=[];index=0
    def click(event,x,y,flags,param):
        if event==cv2.EVENT_LBUTTONDOWN and len(points)<8:points.append([x,y])
    cv2.namedWindow("ROI Calibration");cv2.setMouseCallback("ROI Calibration",click)
    while index<len(roads):
        view=image.copy()
        for i,p in enumerate(points):cv2.circle(view,tuple(p),5,(0,255,255),-1);cv2.putText(view,str(i+1),tuple(p),0,.6,(255,255,255),2)
        cv2.putText(view,f"{roads[index]}: click points | ENTER save | R reset | Q quit",(15,30),0,.7,(255,255,255),2);cv2.imshow("ROI Calibration",view);key=cv2.waitKey(30)&0xFF
        if key==ord("r"):points.clear()
        elif key in (10,13) and len(points)>=3:cfg["roads"][roads[index]]["polygon"]=[[x/cfg["image_width"],y/cfg["image_height"]] for x,y in points];index+=1;points.clear()
        elif key==ord("q"):break
    with open(CONFIG,"w",encoding="utf-8") as f:json.dump(cfg,f,indent=2)
    cv2.destroyAllWindows();print(f"Saved: {CONFIG}")
if __name__=="__main__":calibrate()
