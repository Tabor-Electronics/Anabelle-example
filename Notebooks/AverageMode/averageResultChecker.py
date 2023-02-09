import csv

import numpy as np
import pdb
import os



fft_FILE =  "avgFftNormCount"
wave_FILE =  "avgWaveNormCount"

path = os.path.join(".","results")

#THR = 5

def getDeviation(inlist):
  lnp = np.array(inlist)
  return np.std(lnp)
  
  
  
def analyseFileBatch(fileD, THR):
  maxRes = []
  minRes = []
  meanRes = []
  deltaRes = []
  res = True
  for count, fname in fileD.items():
     with open(fname) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        digArr = np.array([float(row[0]) for row in csv_reader])
        maxRes.append(np.max(digArr))
        minRes.append(np.min(digArr))  
        meanRes.append(np.mean(digArr))  
        deltaRes.append(maxRes[-1]-minRes[-1])  
  ### Compare Normalized results
  maxDev = getDeviation(maxRes)
  minDev = getDeviation(minRes)
  meanDev = getDeviation(meanRes)
  deltaDev = getDeviation(deltaRes)
  if deltaDev > THR:
     res = False
  if maxDev > THR:
     res = False
  if minDev > THR:
     res = False
  if meanDev > THR:
     res = False
  
  return maxRes, maxDev,minRes, minDev, meanRes, meanDev, deltaRes, deltaDev, res

  

def main():

  path = os.path.join(".","results")
  fftFiles = {}
  waveFiles = {}
  for (dirpath, dirnames, filenames) in os.walk(path):
    for filename in filenames:
        if fft_FILE in filename:
            loc = filename.find("NormCount")
            count = int(filename[loc+9:-4])
            fftFiles[count] = os.sep.join([dirpath, filename])
        elif wave_FILE in filename:
            loc = filename.find("NormCount")
            count = int(filename[loc+9:-4])
            waveFiles[count] = os.sep.join([dirpath, filename])
            
  if len(fftFiles)>0:
    maxRes, maxDev,minRes, minDev, meanRes, meanDev, deltaRes, deltaDev, Pass = analyseFileBatch(fftFiles, 312)
    print("== fftFiles Counts:{0}".format(fftFiles.keys()))
    print("maxDev: {:.2f}, Max: {}".format(maxDev,maxRes))
    print("minDev: {:.2f}, Min: {}".format(minDev,minRes))
    print("deltaDev: {:.2f}, delta: {}".format(deltaDev,deltaRes))
    print("meanDev: {:.2f}, Mean: {}".format(meanDev,meanRes))
    print("Pass/Fail: {}".format(Pass))
  if len(waveFiles)>0:
    maxRes, maxDev,minRes, minDev, meanRes, meanDev, deltaRes, deltaDev, Pass = analyseFileBatch(waveFiles, 32)
    print("== waveFiles Counts:{0}".format(fftFiles.keys()))
    print("maxDev: {:.2f}, Max: {}".format(maxDev,maxRes))
    print("minDev: {:.2f}, Min: {}".format(minDev,minRes))
    print("deltaDev: {:.2f}, delta: {}".format(deltaDev,deltaRes))
    print("meanDev: {:.2f}, Mean: {}".format(meanDev,meanRes))
    print("Pass/Fail: {}".format(Pass))
    
if __name__ == "__main__":
  main()
  