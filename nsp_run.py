import atexit
import json
import os
import sys
import gpsMath as gps
import RPi.GPIO as GPIO
import time
import stepperMotor  as step

nsp_settings_path = os.path.dirname(os.path.abspath(__file__)) + "/nsp_settings.json"

class Nsp(object):
    
    def __init__(self):
        self.loadSettings()
        self.nanoPos = self.settings["nanoPos"]
        self.lastPos = self.settings["lastPos"]
        self.target = [float(raw_input("Lat?")), float(raw_input("Lon?"))]
        self.bearing = self.settings["stepperBearing"]
    
    def loadSettings(self):
        self.settings = json.load(open(nsp_settings_path))
    
    def calcBearing(self):
        return gps.calculate_initial_compass_bearing(self.nanoPos,self.target)
        
    def getBearing(self):
        return self.bearing
        
    def displayInfo(self):
        print "NS @ - ", self.nanoPos
        print "Current Bearing ", self.bearing
        print "Last Target @ ", self.lastPos
        print "Target @ ", self.target 
    
def saveSettings(nspObj):
    nspObj.settings["lastPos"] = nspObj.target
    with open(nsp_settings_path,"w") as f:
        f.write(json.dumps(nspObj.settings))
    

myNsp = Nsp()

myNsp.displayInfo()

currentBearing = myNsp.getBearing()
newBearing = myNsp.calcBearing()

myMotor = step.Stepper(currentBearing, newBearing)

turnInstruction = myMotor.dirCalc()

myMotor.turn(turnInstruction)

#saves settings back to .json

atexit.register(saveSettings, myNsp)







