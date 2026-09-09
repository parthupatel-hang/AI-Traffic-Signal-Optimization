"""YOLOv8 detector for road-vehicle detection."""
from pathlib import Path
try:
    import torch
    from ultralytics import YOLO
except Exception as exc:
    torch=None;YOLO=None;_IMPORT_ERROR=exc
else:_IMPORT_ERROR=None

class YOLOVehicleDetector:
    CLASSES={2:"car",3:"motorcycle",5:"bus",7:"truck"}
    def __init__(self,weights="yolov8s.pt",confidence=.50):
        if YOLO is None:raise RuntimeError("Ultralytics/PyTorch is unavailable. Install requirements.txt.") from _IMPORT_ERROR
        root=Path(__file__).resolve().parents[1];requested=Path(weights);local=requested if requested.is_absolute() else root/requested
        self.weights=str(local if local.exists() else requested);self.confidence=float(confidence);self.device="cuda:0" if torch is not None and torch.cuda.is_available() else "cpu";self.model=YOLO(self.weights)
    def detect(self,source):
        detections=[]
        for result in self.model.predict(source=source,conf=self.confidence,device=self.device,verbose=False):
            if result.boxes is None:continue
            for box in result.boxes:
                class_id=int(box.cls.item());name=self.CLASSES.get(class_id)
                if name is None:continue
                detections.append({"class_id":class_id,"class_name":name,"confidence":float(box.conf.item()),"bbox":list(map(int,box.xyxy[0].tolist()))})
        return detections
