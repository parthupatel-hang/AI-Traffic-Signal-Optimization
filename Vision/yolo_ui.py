"""Separate Tkinter window for YOLOv8 image/video detection."""
from pathlib import Path
import threading,tkinter as tk
from tkinter import filedialog,messagebox
import cv2
from PIL import Image,ImageTk
from .yolo_detector import YOLOVehicleDetector

class YOLODetectionWindow:
    IMAGE_EXTS={".jpg",".jpeg",".png",".bmp",".webp"};VIDEO_EXTS={".mp4",".avi",".mov",".mkv",".wmv"}
    def __init__(self,parent):
        self.detector=None;self.window=tk.Toplevel(parent);self.window.title("YOLO Vehicle Detection");self.window.geometry("1050x720");self.window.configure(bg="#111827")
        tk.Label(self.window,text="YOLO VEHICLE DETECTION",fg="white",bg="#111827",font=("Segoe UI",20,"bold")).pack(pady=(18,5));tk.Label(self.window,text="Analyse a traffic image or video with YOLOv8",fg="#9CA3AF",bg="#111827").pack(pady=(0,12))
        bar=tk.Frame(self.window,bg="#111827");bar.pack();tk.Button(bar,text="Select Image / Video",command=self.select_media,bg="#1596DB",fg="white",relief="flat",padx=14,pady=7).pack(side="left",padx=5);tk.Button(bar,text="Close",command=self.window.destroy,bg="#DC2626",fg="white",relief="flat",padx=14,pady=7).pack(side="left",padx=5)
        self.status=tk.Label(self.window,text="Ready.",fg="#D1D5DB",bg="#111827");self.status.pack(pady=8);self.preview=tk.Label(self.window,bg="#0B1020");self.preview.pack(fill="both",expand=True,padx=15,pady=10);self.result=tk.Label(self.window,text="",fg="white",bg="#111827",wraplength=950,font=("Consolas",10,"bold"));self.result.pack(pady=10)
    def select_media(self):
        path=filedialog.askopenfilename(parent=self.window,title="Select traffic media",filetypes=[("Traffic media","*.jpg *.jpeg *.png *.bmp *.webp *.mp4 *.avi *.mov *.mkv *.wmv")])
        if not path:return
        ext=Path(path).suffix.lower()
        if ext in self.IMAGE_EXTS:threading.Thread(target=self._image,args=(path,),daemon=True).start()
        elif ext in self.VIDEO_EXTS:threading.Thread(target=self._video,args=(path,),daemon=True).start()
        else:messagebox.showwarning("Unsupported file","Please choose a supported image or video.",parent=self.window)
    def _get(self):
        if self.detector is None:self.detector=YOLOVehicleDetector()
        return self.detector
    def _image(self,path):
        try:
            self._status("Loading YOLOv8 and analysing image...");d=self._get();r=d.model.predict(path,conf=d.confidence,device=d.device,verbose=False)[0];out_img=r.plot();out=Path(__file__).resolve().parents[1]/"Output"/"detections"/"yolo_detection_result.jpg";out.parent.mkdir(parents=True,exist_ok=True);cv2.imwrite(str(out),out_img);counts={}
            if r.boxes is not None:
                for cls in r.boxes.cls.tolist():name=r.names[int(cls)];counts[name]=counts.get(name,0)+1
            summary=" | ".join(f"{k}: {v}" for k,v in sorted(counts.items())) or "No objects detected";self.window.after(0,lambda:self._show(out_img,summary,out))
        except Exception as e:self._error(e)
    def _video(self,path):
        try:
            self._status("Analysing video...");d=self._get();cap=cv2.VideoCapture(path)
            if not cap.isOpened():raise RuntimeError("Unable to open the selected video.")
            counts={"car":0,"motorcycle":0,"bus":0,"truck":0};frames=0;last=None
            while True:
                ok,frame=cap.read()
                if not ok:break
                r=d.model.predict(frame,conf=d.confidence,device=d.device,verbose=False)[0];last=r.plot();frames+=1
                if r.boxes is not None:
                    for cls in r.boxes.cls.tolist():
                        name=r.names[int(cls)]
                        if name in counts:counts[name]+=1
            cap.release();out=Path(__file__).resolve().parents[1]/"Output"/"detections"/"yolo_video_last_frame.jpg";out.parent.mkdir(parents=True,exist_ok=True)
            if last is not None:cv2.imwrite(str(out),last);summary=f"Frames: {frames} | Cars: {counts['car']} | Motorcycles: {counts['motorcycle']} | Buses: {counts['bus']} | Trucks: {counts['truck']}\nFrame detections are not unique-vehicle counts.";self.window.after(0,lambda:self._show(last,summary,out))
        except Exception as e:self._error(e)
    def _status(self,text):
        try:self.window.after(0,lambda:self.status.config(text=text))
        except tk.TclError:pass
    def _error(self,e):
        self._status("Detection failed.")
        try:self.window.after(0,lambda:messagebox.showerror("YOLO Error",str(e),parent=self.window))
        except tk.TclError:pass
    def _show(self,bgr,summary,out):
        image=Image.fromarray(cv2.cvtColor(bgr,cv2.COLOR_BGR2RGB));image.thumbnail((980,540));photo=ImageTk.PhotoImage(image);self.preview.configure(image=photo);self.preview.image=photo;self.status.config(text=f"Completed. Saved: {out}");self.result.config(text=summary)
