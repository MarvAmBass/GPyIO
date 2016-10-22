#!/usr/bin/python

from os import path
from time import sleep

class GPyIO:

  # gpio true and false
  LOW = 0
  HIGH = 1

  # gpio direction
  IN = "in"
  OUT = "out"

  direction = None



  def __init__(self, gpio):
    self.gpio = gpio

    if not path.isdir("/sys/class/gpio/gpio" + str(self.gpio)):
      exportFile = open("/sys/class/gpio/export","w")
      exportFile.write(str(self.gpio))
      try:
        exportFile.close()
      except:
        #print("closing export filehandle failed")
        pass

    self.direction = self.getDirection()
    if self.direction is None:
      self.setDirection(GPyIO.OUT)

    self.digitalWrite(GPyIO.LOW)


  def getDirection(self):
    directionFileRO = open("/sys/class/gpio/gpio" + str(self.gpio) + "/direction", "r")
    direction = directionFileRO.read()
    try:
      directionFileRO.close()
    except:
      #print("closing direction read only filehandle failed")
      pass

    if direction != GPyIO.IN and direction != GPyIO.OUT:
      direction = None

    return direction



  def setDirection(self, direction):
     if direction != GPyIO.IN and direction != GPyIO.OUT:
       raise ValueError("direction must be either GPyIO.IN or GPyIO.OUT")

      directionFile = open("/sys/class/gpio/gpio" + str(self.gpio) + "/direction","w")
      directionFile.write(direction)
      self.direction = direction
      try:
        directionFile.close()
      except:
        #print("closing export direction failed")
        pass



  def usleep(self, microseconds):
    sleep(microseconds / 1000000.0)



  def digitalWrite(self, value):
    filehandle = open("/sys/class/gpio/gpio" + str(self.gpio) + "/value","w")
    filehandle.write(str(value))
    try:
      filehandle.close()
    except:
      print("filehandle coudn't be closed")



  def digitalWriteSequence(self, valuesString, pulseLengthInMircoseconds):
    for value in valuesString:
      self.digitalWrite(value)
      self.usleep(pulseLengthInMircoseconds)



  def digitalRead(self):
    filehandle = open("/sys/class/gpio/gpio" + str(self.gpio) + "/value","r")
    value = filehandle.read()
    try:
      filehandle.close()
    except:
      print("filehandle coudn't be closed")
    return value



  def digitalReadSequence(self, repetitions, pulseLengthInMircoseconds):
    valuesString = ""
    for i in range(repetitions):
      valuesString += str(self.digitalRead())
      self.usleep(pulseLengthInMircoseconds)
    return valuesString




  def cleanStartingAndEndingLowBytes(self, valuesString):
    signalStarted = False
    cleanFrontString = ""

    for value in valuesString:
      if not signalStarted:
        if value == "1":
            signalStarted = True
      if signalStarted:
        cleanFrontString += value

    # backwards
    reversedCleanString = ""
    signalStarted = False
    for value in reversed(valuesString):
      if not signalStarted:
        if value == "1":
            signalStarted = True
      if signalStarted:
        reversedCleanString += value

    #return reversed reversed cleaned string
    return reversedCleanString[::-1]



if __name__ == '__main__':
  import sys
  if len(sys.argv) == 4:
    #eldo = Eldopy(int(sys.argv[1]))
    #eldo.send433Mhz(sys.argv[2],(sys.argv[3] == 'True'))
  else:
    print("run this script with the following arguments:")
    #print("./eldopy.py gpioNumber AB440CodeString OnOffBoolean")
    #print("")
    #print("example:")
    #print("./eldopy.py 3 11011B True")
    #print("this will switch on 11011B via GPIO Pin 3")
