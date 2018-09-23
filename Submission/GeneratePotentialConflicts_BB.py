#! /usr/bin/env python

#### GeneratePotentialConflicts ####
# Author: William Boler, SEI
# Date: 9/23/2018
# 
# HackTheMachine2018 Track2
#
# Description: This file serves as the first filter in determining potential COLREGS. 
# The space is split into 3D blocks with regards to latitutde, longitude, and time. 
# Blocks in the 3D space are identified as indexed blocks.  Ships within those blocks are
# considered to be potential COLREGS, and are further processed down stream. Two passes are
# executed to ensure overlapping coverage across spaces.  Blocks are hashed and queued, to 
# prevent the search of unnecessary blocks containting 1 or less ships.
#
#### 

import pandas as pd
import math
import argparse
import csv
import numpy as np
import sys
import datetime
from collections import defaultdict


### Class Definitions


class ShipInstance:

  def __init__(self):
    self.index = -1
    self.timeStep = -1
    self.mmsi = str()
    self.lat = -1
    self.lon = -1
    self.basetime = str()
    
  def validate(self):
    if self.index == -1:
      sys.exit('Error, index is -1. ShipInstance')
    if self.timeStep == -1:
      sys.exit('Error, timeStep is -1. ShipInstance')
      
      
  def __eq__(self, other):
    if self.mmsi != other.mmsi:
      return False
    if self.basetime != other.basetime:
      return False
    return True
    
  def __str__(self):
    s = '(ShipInstance{index=' + str(self.index) + ',timestep=' + str(self.timeStep) + ',mmsi=' + \
      self.mmsi + ',lat=' + str(self.lat) + ',lon=' + str(self.lon) + ',basetime=' + self.basetime + '})'
    return s



class ConflictPair:

  def __init__(self):
    self.first = ShipInstance()
    self.second = ShipInstance()
    
  def validate():
    self.first.validate()
    self.second.validate()
    
  def __str__(self):
    s = 'First Id: ' + str(self.first.mmsi) + '\t Second Id: ' + str(self.second.mmsi)
    return s
    
  # TODO May be more complete comparing firsts to seconds as well
  def __eq__(self, other):
    if self.first == other.first:
      return False
    if self.second == other.second:
      return False
    return True
    

  
class BoundingBoxObject:
  
  def __init__(self):
    self.ship = ShipInstance()
    self.boxId = -1
  
  # TODO Broken due to changes, possibly
  def validate(self):
    if not self.shipId:
      sys.exit('Error, shipId is empty. BoundingBoxObject')
    if self.boxId == -1:
      sys.exit('Error, boxId is -1. BoundingBoxObject')
      
  def __str__(self):
    s = '(BoundingBoxObject{ship=' + str(self.ship) + ',boxId=' + str(self.boxId) + '})'
    return s;



class BoundingBoxParameters:

  def __init__(self):
    self.minLatitude = 361
    self.maxLatitude = 361
    self.minLongitude = -90
    self.maxLongitidue = 90
    self.minTimeSeconds = -1
    self.maxTimeSeconds = -1
    self.latCount = -1
    self.lonCount = -1
    self.timeCount = -1
    
    self.latOffset = 0
    self.lonOffset = 0
    self.timeOffset = 0
    
    self._delLat = 1
    self._delLon = 1
    self._delTSeconds = 1
    
  def initialize(self):
    self.validate()
    
    self._delLat = (self.maxLatitude - self.minLatitude) / self.latCount
    self._delLon = (self.maxLongitude - self.minLongitude) / self.lonCount
    self._delTSeconds = (self.maxTimeSeconds - self.minTimeSeconds) / self.timeCount
    
    
  def HashBoundingBoxId(self, lat, lon, t):
    seconds = (pd.to_datetime(t)-datetime.datetime(1970,1,1)).total_seconds()
    
    latIndex = math.trunc( \
      ((float(lat) - self.minLatitude + self.latOffset)/(self.maxLatitude-self.minLatitude)) * self.latCount)
    lonIndex = math.trunc( \
      ((float(lon) - self.minLongitude + self.lonOffset)/(self.maxLongitude-self.minLongitude)) * self.lonCount)         
    timeIndex = math.trunc( \
      ((seconds * self.minTimeSeconds + self.timeOffset)/(self.maxTimeSeconds-self.minTimeSeconds)) * self.timeCount)
    
    # TODO There's a better way to do this
    boxId = \
      latIndex * self.latCount + \
      lonIndex * (self.latCount + self.lonCount) + \
      timeIndex * (self.latCount + self.lonCount +  self.timeCount)
      
    return boxId
      
    #print('Lat: ' + str(lat) + '\tLon: ' + str(lon) + '\tTime: ' + str(seconds) + '\t' + str(latIndex) + ',' + str(lonIndex) + ',' + str(timeIndex) + ': Hash: ' + str(boxId))
    
    
    
  def validate(self):
    #if len(self.size) == 0:
    #  sys.exit('Error, size yet to be insantiated. BoundingBoxParameters')      
    if len(self.startOffset) == 0:
      sys.exit('Error, startOffset yet to be instantiated. BoundingBoxParameters')
    #if len(self.counts) == 0:
    #  sys.exit('Error, counts yet to be instantiated. BoundingBoxParameters')
      
    #if len(self.size) != len(self.startOffset):
      sys.exit('Check dimensions of BoundingBoxParameters: size != startOffset')
    #if len(self.size) != len(self.counts):
      sys.exit('Check dimensions of BoundingBoxParameters: size != counts')
    
    if self.minLatitude > 359:
      sys.exit('Must set minLatitude. BoundingBoxParameters')
    if self.maxLatitude > 359:
      sys.exit('Must set maxLatitude. BoundingBoxParameters')
    # Need checks for latitude
    if self.minTimeSeconds == -1:
      sys.exit('Must set minTimeSeconds. BoundingBoxParameters')
    if self.maxTimeSeconds == -1:
      sys.exit('Must set maxTimeSeconds. BoundingBoxParameters')
      
      



#### Regular Functions



#### vvv THIS IS THE MAIN FUNCTION CALL vvv ####
  
# Load from file and store in memory for now
# TODO how to pass this data?
def GenerateConflictPairs(boundingBoxParameters, inputFile):
  #boundingBoxParameters.validate()
  
  q = list()
  m = defaultdict(list)
  
  finalList = list()
  
  with open(inputFile, 'r') as inputFile:
    reader = csv.DictReader(inputFile, delimiter=',')
    
    for row in reader:
      boxId = boundingBoxParameters.HashBoundingBoxId(row['LAT'],row['LON'],row['BaseDateTime'])
      q.append(boxId)
      s = ShipInstance()
      s.mmsi = row['MMSI']
      s.lat = row['LAT']
      s.lon = row['LON']
      s.basetime = row['BaseDateTime']
      boundingBoxObject = BoundingBoxObject()
      boundingBoxObject.ship = s
      boundingBoxObject.boxId = boxId
      m[boxId].append(boundingBoxObject)
    
    print('Queue Size: ' + str(len(q)))
    
    q.sort()
      
    print('Queue Size After: ' + str(len(q)))
    print('m: ' + str(len(m)))
    
    prevBoxId = None
    for boxId in q:
#      print('BoxId: ' + boxId)
      if boxId == prevBoxId:
        #print('Skip ' + str(boxId))
        continue
      
      prevBoxId = boxId
      boxShipList = m[boxId]
      if len(boxShipList) <= 1:
        continue
      
      # Now, add collision pairs to each other
      # TODO Can be optimized by ignoring duplicate pairs (j = i+1)
      for i,firstShip in enumerate(boxShipList):
        for j,secondShip in enumerate(boxShipList):
          if i <= j:
            continue
          print('First: ' + str(firstShip.ship.mmsi) + '\tSecond: ' + str(secondShip.ship.mmsi))
          if firstShip.ship.mmsi == secondShip.ship.mmsi:
            continue
          conflictPair = ConflictPair()
          conflictPair.first = firstShip.ship
          conflictPair.second = secondShip.ship
          finalList.append(conflictPair)
          
  print('Completed loading data.')
  
  return finalList    
    
    
def PrintCollisions(outputFile, collisions):
  
  print('Printing collisions: size:' + str(len(collisions)))
  
  out = sys.stdout
  if outputFile != None:
    out = open(outputFile, 'w')
      
  header = ['time_1', 'mmsi_1', 'time_2', 'mmsi_2']
  with open(outputFile, 'w') as out:
    csvWriter = csv.writer(out, delimiter=',', lineterminator='\n')
    csvWriter.writerow(header)
    for row in collisions:
      csvWriter.writerow([row.first.basetime, row.first.mmsi, row.second.basetime, row.second.mmsi])
        
  if outputFile != None:
    out.close()
    
  print('Printing complete.')
    


def CreateBoundingBoxParameters(inputFileName, latDivisions, lonDivisions, timeDeltaSeconds, offset=False):
  
  bb = BoundingBoxParameters()
  bb.minLongitude =  float('inf')
  bb.maxLongitude = -float('inf')
  bb.minLatitude =   float('inf')
  bb.maxLatitude =  -float('inf')
  bb.minTimeSeconds =  float('inf')
  bb.maxTimeSeconds = -float('inf')
  bb.latCount = latDivisions
  bb.lonCount = lonDivisions
  
  with open(inputFileName, 'r') as inputFile:
    csvReader = csv.DictReader(inputFile, delimiter=',')
    for row in csvReader:
      bb.minLatitude = min(float(row['LAT']), bb.minLatitude)
      bb.maxLatitude = max(float(row['LAT']), bb.maxLatitude)
      bb.minLongitude = min(float(row['LON']), bb.minLongitude)
      bb.maxLongitude = max(float(row['LON']), bb.maxLongitude)
      seconds = (pd.to_datetime(row['BaseDateTime'])-datetime.datetime(1970,1,1)).total_seconds()
      bb.minTimeSeconds = min(float(seconds), bb.minTimeSeconds)
      bb.maxTimeSeconds = max(float(seconds), bb.maxTimeSeconds)
      
    
  bb.timeCount = (bb.maxTimeSeconds - bb.minTimeSeconds) / (timeDeltaSeconds)
  
  if offset == True:
    bb.latOffset = (bb.maxLatitude - bb.minLatitude) / (2.0 * bb.latCount)
    bb.lonOffset = (bb.maxLongitude - bb.minLongitude) / (2.0 * bb.lonCount)
    bb.timeOffset = (bb.maxTimeSeconds - bb.minTimeSeconds) / (2.0 * bb.timeCount)
  else:
    bb.latOffset = 0
    bb.lonOffset = 0
    bb.timeOffset = 0
  
  return bb

    
def main():
  parser = argparse.ArgumentParser(description='Outputs a list of potential collision pairs based on bounding boxes.')
  parser.add_argument('--inputFile', type=str, default=None, help='Input file.') # TODO Modify for mult
  parser.add_argument('--outputFile', type=str, default='output.csv', help='Output file of pairs and time index.')
  
  args = parser.parse_args()
  
  bb1 = CreateBoundingBoxParameters(args.inputFile, 20, 20, 30, False) # 20 chunks, 20 chunks, 30 seconds
  bb2 = CreateBoundingBoxParameters(args.inputFile, 20, 20, 30, True)
  
  if args.inputFile is None:
    sys.exit('Error, --inputFile not specified.')
    
  print('Loading: ' + args.inputFile)
  
  collisions1 = GenerateConflictPairs(bb1, args.inputFile)
  collisions2 = GenerateConflictPairs(bb2, args.inputFile)
  
  finalList = list()

  for l in collisions1:
    finalList.append(l)
  for l in collisions2:
    duplicate_found = False
    for r in finalList:
      if r == l:
        duplicate_found = True
    if duplicate_found == False:
      finalList.append(l)
  
  
  
  PrintCollisions(args.outputFile, finalList)

    
    
if __name__ == "__main__":
  main()
