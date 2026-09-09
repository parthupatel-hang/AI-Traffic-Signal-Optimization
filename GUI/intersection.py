"""Tkinter four-way intersection simulation and AI control panel."""
import tkinter as tk
from .ai_controller import AIController
from .traffic_lights import TrafficLightController
from .vehicles import CANVAS_H,CANVAS_W,JUNCTION_BOTTOM,JUNCTION_LEFT,JUNCTION_RIGHT,JUNCTION_TOP,STOP_LINE,VehicleManager
from Vision.yolo_ui import YOLODetectionWindow

class Intersection:
    def __init__(self,root):
        self.root=root;self.running=True;self.paused=False;self.use_ai=True;self.weather="Clear";self.time_of_day="Evening"
        self.signal_controller=TrafficLightController();self.vehicle_manager=VehicleManager(None);self.ai_controller=AIController();self.ai_road="N";self.ai_prediction="--";self.ai_confidence=0.0
        frame=tk.Frame(root,bg="#0B1020");frame.pack(fill="both",expand=True)
        self.canvas=tk.Canvas(frame,width=CANVAS_W,height=CANVAS_H,bg="#7CB342",highlightthickness=0);self.canvas.pack(side="left")
        panel=tk.Frame(frame,width=370,bg="#111827",padx=16,pady=16);panel.pack(side="right",fill="y");panel.pack_propagate(False);self.panel=panel
        self.vehicle_manager.canvas=self.canvas;self.stats={};self.lamps={};self._build_panel();self._draw_scene();self._tick()

    def _build_panel(self):
        tk.Label(self.panel,text="AI TRAFFIC SIGNAL\nOPTIMIZATION",fg="white",bg="#111827",font=("Segoe UI",19,"bold"),justify="left").pack(anchor="w")
        tk.Label(self.panel,text="Decision Tree + Adaptive Signal Control",fg="#9CA3AF",bg="#111827",font=("Segoe UI",10)).pack(anchor="w",pady=(0,15))
        controls=tk.Frame(self.panel,bg="#111827");controls.pack(fill="x",pady=(0,15))
        self.pause_btn=tk.Button(controls,text="Pause",command=self.toggle_pause,bg="#2563EB",fg="white",relief="flat");self.pause_btn.pack(side="left",padx=3)
        tk.Button(controls,text="Reset",command=self.reset,bg="#DC2626",fg="white",relief="flat").pack(side="left",padx=3)
        self.ai_btn=tk.Button(controls,text="AI: ON",command=self.toggle_ai,bg="#059669",fg="white",relief="flat");self.ai_btn.pack(side="left",padx=3)
        tk.Button(controls,text="YOLO",command=self.open_yolo,bg="#1596DB",fg="white",relief="flat").pack(side="left",padx=3)
        self._section("Live Status",[("phase","Phase"),("green","Green"),("timer","Timer"),("mode","Mode"),("reason","Switch Reason"),("total","Total Vehicles"),("N","North Queue"),("E","East Queue"),("S","South Queue"),("W","West Queue"),("emergency","Emergency"),("bike","Bikes"),("auto","Auto Rickshaw"),("car","Cars"),("bus","Buses"),("truck","Trucks"),("ambulance","Ambulance")])
        self._section("AI Insights",[("prediction","Predicted Road"),("confidence","Confidence"),("density","Traffic Density"),("congestion","Congestion"),("NW","North Wait"),("EW","East Wait"),("SW","South Wait"),("WW","West Wait"),("weather","Weather"),("tod","Time Of Day")])

    def _section(self,title,rows):
        tk.Label(self.panel,text=title,fg="white",bg="#111827",font=("Segoe UI",12,"bold")).pack(anchor="w",pady=(8,6))
        for key,label in rows:
            row=tk.Frame(self.panel,bg="#111827");row.pack(fill="x",pady=2);tk.Label(row,text=label,fg="#D1D5DB",bg="#111827",font=("Segoe UI",9)).pack(side="left")
            self.stats[key]=tk.StringVar(value="--");tk.Label(row,textvariable=self.stats[key],fg="white",bg="#111827",font=("Consolas",9,"bold")).pack(side="right")

    def _draw_scene(self):
        c=self.canvas;c.create_rectangle(0,350,CANVAS_W,550,fill="#2F343A",outline="");c.create_rectangle(420,0,620,CANVAS_H,fill="#2F343A",outline="");c.create_rectangle(JUNCTION_LEFT,JUNCTION_TOP,JUNCTION_RIGHT,JUNCTION_BOTTOM,outline="#FACC15",width=2)
        for y in (420,480):c.create_line(0,y,370,y,fill="white",dash=(14,12),width=2);c.create_line(670,y,CANVAS_W,y,fill="white",dash=(14,12),width=2)
        for x in (490,550):c.create_line(x,0,x,300,fill="white",dash=(14,12),width=2);c.create_line(x,600,x,CANVAS_H,fill="white",dash=(14,12),width=2)
        for text,pos in (("NORTH",(520,30)),("SOUTH",(520,870)),("EAST",(1000,450)),("WEST",(40,450))):c.create_text(*pos,text=text,fill="white",font=("Segoe UI",14,"bold"))
        c.create_line(420,STOP_LINE["N"],620,STOP_LINE["N"],fill="white",width=4);c.create_line(420,STOP_LINE["S"],620,STOP_LINE["S"],fill="white",width=4);c.create_line(STOP_LINE["W"],350,STOP_LINE["W"],550,fill="white",width=4);c.create_line(STOP_LINE["E"],350,STOP_LINE["E"],550,fill="white",width=4)
        for d,(x,y) in {"N":(550,645),"S":(490,255),"E":(325,480),"W":(715,420)}.items():self.lamps[d]=c.create_oval(x-16,y-16,x+16,y+16,fill="red",outline="#111827",width=2)

    @staticmethod
    def _density_level(total):return "Low" if total<=12 else "Medium" if total<=25 else "High"
    @staticmethod
    def _congestion(d,w):
        q,wait=max(d.values()),max(w.values());return "High" if q>=12 or wait>=40 else "Medium" if q>=6 or wait>=20 else "Low"

    def _features(self,emergency,direction):
        d=self.vehicle_manager.get_density();w=self.vehicle_manager.get_average_waiting_times();e={"N":"North","E":"East","S":"South","W":"West"}.get(direction,"None") if emergency else "None"
        return {"NorthVehicles":d["N"],"SouthVehicles":d["S"],"EastVehicles":d["E"],"WestVehicles":d["W"],"NorthWaitingTime":w["N"],"SouthWaitingTime":w["S"],"EastWaitingTime":w["E"],"WestWaitingTime":w["W"],"TimeOfDay":self.time_of_day,"Weather":self.weather,"Emergency":e,"TrafficDensity":self._density_level(sum(d.values())),"CongestionLevel":self._congestion(d,w),"GreenSignalTime":self.signal_controller.get_remaining_green_seconds()}

    def _predict(self,emergency,direction):
        try:self.ai_prediction,self.ai_confidence=self.ai_controller.predict_best_road(self._features(emergency,direction));self.ai_road={"North":"N","East":"E","South":"S","West":"W"}.get(self.ai_prediction,"N")
        except Exception:self.ai_prediction,self.ai_confidence,self.ai_road="ERR",0.0,"N"

    def _update_stats(self,emergency,direction):
        d=self.vehicle_manager.get_density();w=self.vehicle_manager.get_average_waiting_times();counts=self.vehicle_manager.get_vehicle_type_counts();vals={"phase":self.signal_controller.get_phase(),"green":self.signal_controller.get_current_green_direction(),"timer":f"{self.signal_controller.get_remaining_green_seconds()} sec","mode":"AI" if self.use_ai else "FIXED","reason":self.signal_controller.get_last_reason(),"total":self.vehicle_manager.get_total_count(),**d,"emergency":({"N":"North","E":"East","S":"South","W":"West"}.get(direction,"None") if emergency else "None"),**counts,"prediction":self.ai_prediction,"confidence":f"{self.ai_confidence:.1f}%","density":self._density_level(sum(d.values())),"congestion":self._congestion(d,w),"NW":f"{w['N']:.1f}s","EW":f"{w['E']:.1f}s","SW":f"{w['S']:.1f}s","WW":f"{w['W']:.1f}s","weather":self.weather,"tod":self.time_of_day}
        for key,value in vals.items():
            if key in self.stats:self.stats[key].set(str(value))
        for road,state in self.signal_controller.get_states().items():self.canvas.itemconfig(self.lamps[road],fill={"GREEN":"#22C55E","YELLOW":"#FACC15"}.get(state,"#DC2626"))

    def _tick(self):
        if not self.running:return
        if not self.paused:
            emergency,direction=self.vehicle_manager.emergency_present()
            if self.use_ai:self._predict(emergency,direction);self.signal_controller.ai_control(self.vehicle_manager.get_density(),self.vehicle_manager.get_average_waiting_times(),self.ai_road,emergency,direction,30)
            else:self.signal_controller.automatic_cycle(30)
            self.vehicle_manager.update(self.signal_controller.get_states());self._update_stats(emergency,direction)
        self.root.after(30,self._tick)

    def toggle_pause(self):self.paused=not self.paused;self.pause_btn.config(text="Resume" if self.paused else "Pause")
    def toggle_ai(self):self.use_ai=not self.use_ai;self.ai_btn.config(text=f"AI: {'ON' if self.use_ai else 'OFF'}",bg="#059669" if self.use_ai else "#B45309")
    def reset(self):self.vehicle_manager.clear();self.signal_controller=TrafficLightController();self.ai_prediction="--";self.ai_confidence=0.0;self.ai_road="N"
    def open_yolo(self):YOLODetectionWindow(self.root)
    def stop(self):self.running=False;self.vehicle_manager.clear()
