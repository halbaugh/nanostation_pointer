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
        if("gps" in raw_input("Gps or Bearing mode?")):
            self.target = [float(raw_input("Lat?")), float(raw_input("Lon?"))]
            self.runMode = "gps"
        else:
            self.runMode = "bearing"
            self.targetBearing = int(raw_input("Bearing?"))
        self.bearing = self.settings["stepperBearing"]
    
    def loadSettings(self):
        self.settings = json.load(open(nsp_settings_path))
    
    def calcBearing(self):
        return gps.calculate_initial_compass_bearing(self.nanoPos,self.target)
        
    def getBearing(self):
        return self.bearing
        
    def setBearing(self,bearing):
        self.bearing = bearing
        
    def getTargetBearing(self):
        return self.targetBearing
        
    def setTargetBearing(self,bearing):
        self.targetBearing = bearing
        
    def displayInfo(self):
        if("gps" in myNsp.runMode):
            print "NS @ - ", self.nanoPos
            print "Current Bearing ", self.bearing
            print "Last Target @ ", self.lastPos
            print "New Target @ ", self.target
        if("bearing" in myNsp.runMode):
            print "Current Bearing ", self.bearing
            print "Target Bearing ", self.targetBearing
    
def saveSettings(nspObj):
    if("gps" in myNsp.runMode):
        nspObj.settings["lastPos"] = nspObj.target
    print "saving target bearing:", nspObj.targetBearing
    nspObj.settings["stepperBearing"] = nspObj.targetBearing
    
    with open(nsp_settings_path,"w") as f:
        f.write(json.dumps(nspObj.settings))
    

myNsp = Nsp()
if("gps" in myNsp.runMode):
    
    
    myNsp.displayInfo()
    
    myNsp.setTargetBearing(myNsp.calcBearing())
    print "new calculated bearing is ", myNsp.getTargetBearing()
    myMotor = step.Stepper(myNsp.getBearing()   , myNsp.getTargetBearing())
    print "Made my motor."
    
    turnInstruction = myMotor.dirCalc()
    print "calculated turnInstruction"
    
    myMotor.turn(turnInstruction)
    print "Told motor to turn."
    #saves settings back to .json
    
    atexit.register(saveSettings, myNsp)
    print "Saved stats and exited."
    
if("bearing" in myNsp.runMode):
    myNsp.displayInfo()
    print "cur bearing:tar bearing --- ", myNsp.getBearing(), myNsp.getTargetBearing()
    myMotor = step.Stepper(myNsp.getBearing(), myNsp.getTargetBearing())
    print "Made my motor."
    
    turnInstruction = myMotor.dirCalc()
    turnInstruction.append("bearing")
    print "calculated turnInstruction"
    
    myMotor.turn(turnInstruction)
    print "Told motor to turn."
    #saves settings back to .json
    
    atexit.register(saveSettings, myNsp)
    print "Saved stats and exited."
    






