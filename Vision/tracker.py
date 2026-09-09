"""Centroid-based tracker with persistent IDs and speed estimates."""
import math,time
class CentroidTracker:
    def __init__(self,max_distance=90,max_missed=12):self.max_distance=max_distance;self.max_missed=max_missed;self.next_id=1;self.objects={}
    def update(self,detections,now=None):
        now=time.time() if now is None else now;used=set();result=[]
        for d in detections:
            x1,y1,x2,y2=d["bbox"];cx,cy=(x1+x2)/2,(y1+y2)/2;best=None;best_dist=self.max_distance
            for oid,o in self.objects.items():
                if oid not in used and o["class_name"]==d["class_name"]:
                    dist=math.hypot(cx-o["cx"],cy-o["cy"])
                    if dist<best_dist:best,best_dist=oid,dist
            if best is None:
                oid=self.next_id;self.next_id+=1;speed=0.0;self.objects[oid]={"cx":cx,"cy":cy,"class_name":d["class_name"],"last":now,"missed":0,"first":now}
            else:
                oid=best;o=self.objects[oid];elapsed=max(now-o["last"],1e-3);speed=math.hypot(cx-o["cx"],cy-o["cy"])/elapsed;o.update(cx=cx,cy=cy,last=now,missed=0)
            used.add(oid);item=dict(d);item.update(track_id=oid,center=[cx,cy],speed_px_s=speed);result.append(item)
        for oid in list(self.objects):
            if oid not in used:
                self.objects[oid]["missed"]+=1
                if self.objects[oid]["missed"]>self.max_missed:del self.objects[oid]
        return result
