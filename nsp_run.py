import atexit
import json
import os
import sys
import gpsMath as gps

nsp_settings_path = os.path.dirname(os.path.abspath(__file__)) + "/nsp_settings.json"

class Nsp(object):
    
    def __init__(self):
        self.loadSettings()
        self.nanoPos = self.settings["nanoPos"]
        self.lastPos = self.settings["lastPos"]
        self.target = [float(raw_input("Lat?")), float(raw_input("Lon?"))]
    
    def loadSettings(self):
        self.settings = json.load(open(nsp_settings_path))
    
    def calcBearing(self):
        return gps.calculate_initial_compass_bearing(self.nanoPos,self.target)
        
    def displayInfo(self):
        print "NS @ - ", self.nanoPos
        print "Last Target @ - ", self.lastPos
        print "Target @ ", self.target
    
    
def saveSettings(nspObj):
    nspObj.settings["lastPos"] = nspObj.target
    with open(nsp_settings_path,"w") as f:
        f.write(json.dumps(nspObj.settings))
    

    
myNsp = Nsp()

myNsp.displayInfo()
newBearing = myNsp.calcBearing()

#saves settings back to .json

atexit.register(saveSettings, myNsp)







