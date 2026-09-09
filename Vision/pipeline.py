"""End-to-end YOLO detection, tracking, road assignment and traffic scoring."""
from pathlib import Path
import time,cv2
from .adaptive_controller import AdaptiveSignalController
from .road_assigner import RoadAssigner
from .tracker import CentroidTracker
from .traffic_metrics import TrafficMetrics
from .yolo_detector import YOLOVehicleDetector
class TrafficPipeline:
    def __init__(self,project_root):
        root=Path(project_root);self.detector=YOLOVehicleDetector(root/"yolov8s.pt");self.assigner=RoadAssigner(root/"Input"/"config"/"road_config.json");self.tracker=CentroidTracker();self.metrics=TrafficMetrics();self.controller=AdaptiveSignalController();self.weather="Clear";self.emergency_road=None
    def set_context(self,weather="Clear",emergency_road=None):self.weather=weather;self.emergency_road=emergency_road
    def process(self,frame,now=None):
        now=time.time() if now is None else now;detections=self.tracker.update(self.detector.detect(frame),now);detections=[self.assigner.assign_detection(d) for d in detections];metrics=self.metrics.calculate(detections,now,self.weather,self.emergency_road);road,green=self.controller.choose(metrics);out=frame.copy()
        for name,p in self.assigner.polygons.items():cv2.polylines(out,[p],True,(255,255,255),2);cv2.putText(out,name,tuple(p[0]),0,.7,(255,255,255),2)
        for d in detections:
            x1,y1,x2,y2=d["bbox"];cv2.rectangle(out,(x1,y1),(x2,y2),(0,255,0),2);cv2.putText(out,f"ID {d['track_id']} {d['class_name']} [{d['road']}]",(x1,max(20,y1-5)),0,.5,(0,255,0),2)
        cv2.putText(out,f"AI GREEN: {road} | {green}s",(20,40),0,.8,(0,255,0),2);return out,metrics,road,green,detections
