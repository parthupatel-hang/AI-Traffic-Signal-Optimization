"""Run the vision pipeline on a webcam or video source."""
import cv2
class VideoRunner:
    def __init__(self,pipeline):self.pipeline=pipeline
    def run(self,source=0):
        cap=cv2.VideoCapture(source)
        if not cap.isOpened():raise RuntimeError(f"Cannot open video source: {source}")
        try:
            while True:
                ok,frame=cap.read()
                if not ok:break
                out,metrics,road,green,_=self.pipeline.process(frame);cv2.putText(out,f"AI GREEN: {road} | {green}s",(20,40),0,1,(0,255,0),2);cv2.imshow("AI Traffic Signal Optimization",out)
                if cv2.waitKey(1)&0xFF==ord("q"):break
        finally:cap.release();cv2.destroyAllWindows()
