"""Queue, waiting-time, density and priority metrics for each road."""
import datetime,time
ROADS=("NORTH","SOUTH","EAST","WEST")
class TrafficMetrics:
    def __init__(self):self.first_seen={}
    def calculate(self,detections,now=None,weather="Clear",emergency_road=None):
        now=time.time() if now is None else now;m={r:{"count":0,"queue_length":0,"waiting_time_s":0.0,"density_pct":0.0,"score":0.0,"emergency":r==emergency_road,"weather":weather,"peak_hour":False} for r in ROADS}
        peak=datetime.datetime.fromtimestamp(now).hour in list(range(7,10))+list(range(17,21))
        for d in detections:
            r=d.get("road");tid=d.get("track_id")
            if r not in m:continue
            m[r]["count"]+=1
            if tid is not None:
                self.first_seen.setdefault(tid,now)
                if d.get("speed_px_s",0)<25:m[r]["queue_length"]+=1;m[r]["waiting_time_s"]=max(m[r]["waiting_time_s"],now-self.first_seen[tid])
        factor={"Clear":1.0,"Cloudy":1.05,"Rain":1.15,"Fog":1.20}.get(weather,1.0)
        for r in ROADS:
            c,q,w=m[r]["count"],m[r]["queue_length"],m[r]["waiting_time_s"];m[r]["density_pct"]=min(100,c/20*100)
            base=.35*min(c/20,1)+.25*min(q/12,1)+.20*min(w/120,1)+.10*m[r]["density_pct"]/100
            m[r]["score"]=min(1,base*factor+(.10 if peak else 0)+(.35 if m[r]["emergency"] else 0));m[r]["peak_hour"]=peak
        return m
