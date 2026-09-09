"""Adaptive green-road recommendation from vision metrics."""
class AdaptiveSignalController:
    def __init__(self,min_green=10,max_green=60,yellow=3):self.min_green=min_green;self.max_green=max_green;self.yellow=yellow
    def choose(self,metrics):
        road=max(metrics,key=lambda r:metrics[r]["score"]);score=metrics[road]["score"];green=round(self.min_green+(self.max_green-self.min_green)*score)
        return road,max(self.min_green,min(self.max_green,green))
