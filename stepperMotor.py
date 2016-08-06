import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False) 

class Stepper(object):
  #initializes the motor
  #requires current bearing and new bearing
  #can be set later on if needed
  def __init__(self,cur,target):
    
    GPIO.setmode(GPIO.BCM)
 
    self.enable_pin = 18
    self.coil_A_1_pin = 4
    self.coil_A_2_pin = 17
    self.coil_B_1_pin = 23
    self.coil_B_2_pin = 24
    
    
    GPIO.setup(self.enable_pin, GPIO.OUT)
    GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
    GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
    GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
    GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
     
    GPIO.output(self.enable_pin, 1)
    
    self.currentBearing = cur
    self.targetBearing = target
    print "end of motor init"  
 
  def turnClockwise(self,delay, steps):
    print "in turnClockwise.", steps
    for i in range(0, steps):
      self.setStep(1, 0, 0, 1)
      time.sleep(delay)
      self.setStep(0, 1, 0, 1)
      time.sleep(delay)
      self.setStep(0, 1, 1, 0)
      time.sleep(delay)
      self.setStep(1, 0, 1, 0)
      time.sleep(delay)
 
  def turnCounterclockwise(self, delay, steps):
    print "in turnCounterclockwise.", steps
    for i in range(0, steps):
      self.setStep(1, 0, 1, 0)
      time.sleep(delay)
      self.setStep(0, 1, 1, 0)
      time.sleep(delay)
      self.setStep(0, 1, 0, 1)
      time.sleep(delay)
      self.setStep(1, 0, 0, 1)
      time.sleep(delay)
 
  
  def setStep(self, w1, w2, w3, w4):
    print "Setting step in setStep."
    GPIO.output(self.coil_A_1_pin, w1)
    GPIO.output(self.coil_A_2_pin, w2)
    GPIO.output(self.coil_B_1_pin, w3)
    GPIO.output(self.coil_B_2_pin, w4)

  def setCurrentBearing(self,val):
    self.currentBearing = val
    
  def getCurrentBearing(self):
    return self.currentBearing
    
  def setTargetBearing(self,val):
    self.targetBearing = val
    
  def getTargetBearing(self):
    return self.targetBearing
  
  #calculates the shortest direction to go it
  #returns a list of (string(direction),int(degreeBearing))
  def dirCalc(self):
    cur = self.currentBearing
    tar = self.targetBearing
    
    turnDegree = 0
    turnDirection = ""
    
    if(cur > tar):
      turnDegree = cur - tar
      turnDirection = "counterclockwise"
      if(turnDegree > 180):
        turnDegree = 180 - (turnDegree - 180)
        turnDirection = "clockwise"
    else:
      turnDegree = tar - cur
      turnDirection = "clockwise"
      if(turnDegree > 180):
        turnDegree = 180 - (turnDegree - 180)
        turnDirection = "counterclockwise"
        
    turnInstruction = [turnDirection, turnDegree]
    print "returning turnInstruction:" , turnInstruction
    return turnInstruction
    
  #Turns the motor to the new bearing
  #Converts Degrees to Steps and then runs
  def turn(self,turnInstruction):
    delay = .01
    steps = int((turnInstruction[1]/360)*512)
    print "In myMotor.turn with turn instructions:", turnInstruction
    print "Converted to steps: ", steps
    if("clockwise" in turnInstruction[0]):
      self.turnClockwise(delay,steps)
    else:
      self.turnCounterclockwise(delay,steps)
      
  
