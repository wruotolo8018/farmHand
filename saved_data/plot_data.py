# Imports
import numpy as np
from plotter import plotData
import os

folderName = "./"
fileNameList = os.listdir(folderName)

fileNameList.sort()

# Print all files in that folder for selection
print()
for i in range(len(fileNameList)):
    print(str(i) + ": " + str(fileNameList[i]))

# Allocate fileName
fileIndex = int(input("\n\nSelect Index of file you want to test filter on: "))
fileName = folderName + fileNameList[fileIndex]

data_array = np.load(fileName)
plotData(data_array[:,1:])