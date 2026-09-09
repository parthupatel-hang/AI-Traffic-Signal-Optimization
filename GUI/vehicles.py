"""Four-way traffic simulation with straight movement and free-left turns."""
import math
import random

CANVAS_W, CANVAS_H = 1040, 900
CENTER_X, CENTER_Y = 520, 450
JUNCTION_LEFT, JUNCTION_RIGHT, JUNCTION_TOP, JUNCTION_BOTTOM = 370, 670, 300, 600
STOP_LINE = {"N":270,"S":630,"E":700,"W":340}
LANES = {"N":(550,-70),"S":(490,CANVAS_H+70),"E":(CANVAS_W+70,480),"W":(-70,420)}
OUT = {"N":(550,CANVAS_H+120),"S":(490,-120),"E":(-120,480),"W":(CANVAS_W+120,420)}

class Vehicle:
    TYPES=("bike","auto","car","bus","truck","ambulance")
    SPEED={"bike":3.2,"auto":2.7,"car":2.8,"ambulance":3.6,"bus":2.0,"truck":1.9}
    def __init__(self,canvas,direction,vehicle_type,route="STRAIGHT"):
        self.canvas,self.direction,self.vehicle_type,self.route_type=canvas,direction,vehicle_type,route
        self.speed=self.current_speed=self.SPEED[vehicle_type]; self.wait_time=0.0; self.currently_waiting=False
        self.has_crossed=False; self.finished=False; self.x,self.y=LANES[direction]; self.parts=[]
        self.color=random.choice(("#E53935","#1E88E5","#43A047","#FB8C00","#8E24AA","#546E7A")); self._draw()
    def _draw(self):
        fill={"ambulance":"white","bike":"#37474F","auto":"#2E7D32","bus":"#1976D2","truck":"#757575"}.get(self.vehicle_type,self.color)
        w,h=(22,12) if self.direction in ("E","W") else (12,22)
        self.parts=[self.canvas.create_rectangle(self.x-w,self.y-h,self.x+w,self.y+h,fill=fill,outline="#111",width=2)]
        if self.vehicle_type=="ambulance":
            self.parts += [self.canvas.create_line(self.x-7,self.y,self.x+7,self.y,fill="red",width=3),self.canvas.create_line(self.x,self.y-7,self.x,self.y+7,fill="red",width=3)]
    def _move(self,dx,dy):
        for part in self.parts:self.canvas.move(part,dx,dy)
        self.x+=dx;self.y+=dy
    def destroy(self):
        for part in self.parts:self.canvas.delete(part)
        self.parts.clear()
    def at_stop_line(self):
        if self.has_crossed or self.route_type!="STRAIGHT": return False
        return {"N":self.y>=STOP_LINE["N"]-8,"S":self.y<=STOP_LINE["S"]+8,"E":self.x<=STOP_LINE["E"]+8,"W":self.x>=STOP_LINE["W"]-8}[self.direction]
    def update(self,stopped=False,dt=.03):
        if stopped:
            self.currently_waiting=not self.has_crossed and self.route_type=="STRAIGHT"
            if self.currently_waiting:self.wait_time+=dt
            self.current_speed=max(0,self.current_speed-.2)
        else:self.currently_waiting=False;self.current_speed=min(self.speed,self.current_speed+.08)
        if self.route_type=="FREE_LEFT":
            target={"N":(640,380),"E":(590,720),"S":(260,520),"W":(450,180)}[self.direction];dx,dy=target[0]-self.x,target[1]-self.y;dist=max(math.hypot(dx,dy),1);self._move(dx/dist*self.current_speed,dy/dist*self.current_speed);self.finished=dist<8;return
        dx,dy=0,0
        if self.direction=="N":dy=self.current_speed
        elif self.direction=="S":dy=-self.current_speed
        elif self.direction=="E":dx=-self.current_speed
        else:dx=self.current_speed
        self._move(dx,dy)
        if self.direction=="N" and self.y>JUNCTION_BOTTOM:self.has_crossed=True
        if self.direction=="S" and self.y<JUNCTION_TOP:self.has_crossed=True
        if self.direction=="E" and self.x<JUNCTION_LEFT:self.has_crossed=True
        if self.direction=="W" and self.x>JUNCTION_RIGHT:self.has_crossed=True
        ox,oy=OUT[self.direction];self.finished=math.hypot(self.x-ox,self.y-oy)<80

class VehicleManager:
    def __init__(self,canvas):self.canvas=canvas;self.vehicles=[];self.frame=0;self.spawn_interval=22;self.max_vehicles=60
    def spawn_vehicle(self):
        if len(self.vehicles)>=self.max_vehicles:return
        d=random.choice(("N","E","S","W"));r="FREE_LEFT" if random.random()<.30 else "STRAIGHT";t=random.choices(Vehicle.TYPES,weights=(34,20,28,7,7,4))[0];v=Vehicle(self.canvas,d,t,r)
        if any(x.direction==d and math.hypot(x.x-v.x,x.y-v.y)<90 for x in self.vehicles):v.destroy();return
        self.vehicles.append(v)
    def update(self,states):
        self.frame+=1
        if self.frame>=self.spawn_interval:self.frame=0;self.spawn_vehicle()
        for v in list(self.vehicles):
            v.update(v.at_stop_line() and states.get(v.direction)!="GREEN")
            if v.finished:v.destroy();self.vehicles.remove(v)
    def clear(self):
        for v in self.vehicles:v.destroy()
        self.vehicles.clear()
    def get_density(self):return {d:sum(v.direction==d and not v.has_crossed and v.route_type=="STRAIGHT" for v in self.vehicles) for d in ("N","E","S","W")}
    def get_total_count(self):return len(self.vehicles)
    def emergency_present(self):
        for v in self.vehicles:
            if v.vehicle_type=="ambulance" and v.route_type=="STRAIGHT" and not v.has_crossed:return True,v.direction
        return False,None
    def get_vehicle_type_counts(self):return {t:sum(v.vehicle_type==t for v in self.vehicles) for t in Vehicle.TYPES}
    def get_average_waiting_times(self):
        out={d:0.0 for d in ("N","E","S","W")};groups={d:[] for d in out}
        for v in self.vehicles:
            if v.currently_waiting:groups[v.direction].append(v.wait_time)
        for d,x in groups.items():
            if x:out[d]=sum(x)/len(x)
        return out
