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
        self.currentBearing = self.settings["stepperBearing"]
        self.target = [float(raw_input("Lat?")), float(raw_input("Lon?"))]
    
    def loadSettings(self):
        self.settings = json.load(open(nsp_settings_path))
    
    def calcBearing(self):
        self.newBearing = gps.calculate_initial_compass_bearing(self.nanoPos,self.target)
        
    def displayInfo(self):
        print "NS @ ", self.nanoPos
        print "Last Target @ ", self.lastPos
        print "Current Bearing @ ", self.currentBearing
        print ""
        print "New Target @ ", self.target
        print "New Bearing @ ", self.newBearing
    
    
def saveSettings(nspObj):
    nspObj.settings["lastPos"] = nspObj.target
    nspObj.settings["stepperBearing"] = nspObj.newBearing
    with open(nsp_settings_path,"w") as f:
        f.write(json.dumps(nspObj.settings))
    
    
myNsp = Nsp()
myNsp.calcBearing()
myNsp.displayInfo()


atexit.register(saveSettings, myNsp)







