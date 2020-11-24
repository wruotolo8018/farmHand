# Imports
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import style

ribbed_folderName = "./two_phalange_data_ribbed_pinch/"
control_folderName = "./two_phalange_data_control_pinch/"

# Change this to change folders
folderName = control_folderName
folderName2 = ribbed_folderName

fileNameList = os.listdir(folderName)
fileNameList.sort()

fileNameList2 = os.listdir(folderName2)
fileNameList2.sort()

# Print all files in that folder for selection
# print()
# for i in range(len(fileNameList)):
#     print(str(i) + ": " + str(fileNameList[i]))

# Allocate fileName
# fileIndex = int(input("\n\nSelect Index of file you want to test filter on: "))
# fileName = folderName + fileNameList[fileIndex]

fileNameC0 = folderName + fileNameList[1]
fileNameCS = folderName + fileNameList[2]
fileNameCL = folderName + fileNameList[3]

fileNameR0 = folderName2 + fileNameList2[11]
fileNameRS = folderName2 + fileNameList2[10]
fileNameRL = folderName2 + fileNameList2[7]

data_arrayR0 = np.load(fileNameR0)
data_arrayR0 = data_arrayR0[:, 215:]
# print(np.shape(data_arrayR0))
data_arrayRS = np.load(fileNameRS)
data_arrayRS = data_arrayRS[:, 90:278]
data_arrayRL = np.load(fileNameRL)
data_arrayRL = data_arrayRL[:, 100:]

data_arrayC0 = np.load(fileNameC0)
data_arrayC0 = data_arrayC0[:, 199:247] #247
# print(np.shape(data_arrayR0))
data_arrayCS = np.load(fileNameCS)
data_arrayCS = data_arrayCS[:, 110:248] #248
data_arrayCL = np.load(fileNameCL)
data_arrayCL = data_arrayCL[:, 95:212] #230

# data_array = np.concatenate(data_arrayR0,data_arrayRS,data_arrayRL)
# print(data_arrayR0)
# plotData(data_array[:,1:])

style.use('fivethirtyeight')
fig, (R0Plot, RSPlot, RLPlot) = plt.subplots(nrows=1, ncols=3)

# print("repArray.shape: " + str(repArray.shape))

# plotArrayFloat = np.array([[float(x) for x in y] for y in data_arrayR0])
plotArrayFloatR0 = data_arrayR0
plotArrayFloatRS = data_arrayRS
plotArrayFloatRL = data_arrayRL

plotArrayFloatC0 = data_arrayC0
plotArrayFloatCS = data_arrayCS
plotArrayFloatCL = data_arrayCL

m2cm = 100

dispR0 = plotArrayFloatR0[2, :]
dispSizeR0 = np.shape(dispR0)
dispOffsetR0 = np.ones(dispSizeR0)*dispR0[0]
dispR0 = dispR0 - dispOffsetR0
dispR0 = m2cm*dispR0

dispRS = plotArrayFloatRS[2, :]
dispSizeRS = np.shape(dispRS)
dispOffsetRS = np.ones(dispSizeRS)*dispRS[0]
dispRS = dispRS - dispOffsetRS
dispRS = m2cm*dispRS

dispRL = plotArrayFloatRL[2, :]
dispSizeRL = np.shape(dispRL)
dispOffsetRL = np.ones(dispSizeRL)*dispRL[0]
dispRL = dispRL - dispOffsetRL
dispRL = m2cm*dispRL

dispC0 = plotArrayFloatC0[2, :]
dispSizeC0 = np.shape(dispC0)
dispOffsetC0 = np.ones(dispSizeC0)*dispC0[0]
dispC0 = dispC0 - dispOffsetC0
dispC0 = m2cm*dispC0

dispCS = plotArrayFloatCS[2, :]
dispSizeCS = np.shape(dispCS)
dispOffsetCS = np.ones(dispSizeCS)*dispCS[0]
dispCS = dispCS - dispOffsetCS
dispCS = m2cm*dispCS

dispCL = plotArrayFloatCL[2, :]
dispSizeCL = np.shape(dispCL)
dispOffsetCL = np.ones(dispSizeCL)*dispCL[0]
dispCL = dispCL - dispOffsetCL
dispCL = m2cm*dispCL

phal1DataR0 = plotArrayFloatR0[0, :]
phal2DataR0 = plotArrayFloatR0[1, :]

phal1DataRS = plotArrayFloatRS[0, :]
phal2DataRS = plotArrayFloatRS[1, :]

phal1DataRL = plotArrayFloatRL[0, :]
phal2DataRL = plotArrayFloatRL[1, :]

phal1DataC0 = plotArrayFloatC0[0, :]
phal2DataC0 = plotArrayFloatC0[1, :]

phal1DataCS = plotArrayFloatCS[0, :]
phal2DataCS = plotArrayFloatCS[1, :]

phal1DataCL = plotArrayFloatCL[0, :]
phal2DataCL = plotArrayFloatCL[1, :]

R0Plot.clear()
R0Plot.plot(dispR0, phal1DataR0, 'v', color='green')
R0Plot.plot(dispR0, phal2DataR0, '^', color='black')
R0Plot.plot(dispC0, phal1DataC0, 'o')
R0Plot.plot(dispC0, phal2DataC0, 'o')
R0Plot.set_ylim(-0.5, 10.5)
R0Plot.set_xlim(-0.0005*m2cm, 0.0105*m2cm)
R0Plot.set_xlabel('Displacement (cm)')
R0Plot.set_ylabel('Force (N)')

RSPlot.clear()
RSPlot.plot(dispRS, phal1DataRS, 'v', color='green')
RSPlot.plot(dispRS, phal2DataRS, '^', color='black')
RSPlot.plot(dispCS, phal1DataCS, 'o')
RSPlot.plot(dispCS, phal2DataCS, 'o')
RSPlot.set_ylim(-0.5, 10.5)
RSPlot.set_xlim(-0.0005*m2cm, 0.0105*m2cm)
RSPlot.set_xlabel('Displacement (cm)')
RSPlot.set_ylabel('Force (N)')

RLPlot.clear()
RLPlot.plot(dispRL, phal1DataRL, 'v', color='green')
RLPlot.plot(dispRL, phal2DataRL, '^', color='black')
RLPlot.plot(dispCL, phal1DataCL, 'o')
RLPlot.plot(dispCL, phal2DataCL, 'o')
RLPlot.set_ylim(-0.5, 10.5)
RLPlot.set_xlim(-0.0005*m2cm, 0.0105*m2cm)
RLPlot.set_xlabel('Displacement (cm)')
RLPlot.set_ylabel('Force (N)')

R0Plot.title.set_text('0 Offset')
RSPlot.title.set_text('Small Offset')
RLPlot.title.set_text('Large Offset')

# C0Plot.clear()
# C0Plot.plot(dispC0, phal1DataC0, 'o')
# C0Plot.plot(dispC0, phal2DataC0, 'o')
# C0Plot.set_ylim(-0.5, 10.5)
# # C0Plot.set_xlim(-0.5, 10.5)
# C0Plot.set_xlabel('Displacement (cm)')
# C0Plot.set_ylabel('Force (N)')
#
# CSPlot.clear()
# CSPlot.plot(dispCS, phal1DataCS, 'o')
# CSPlot.plot(dispCS, phal2DataCS, 'o')
# CSPlot.set_ylim(-0.5, 10.5)
# # CSPlot.set_xlim(-0.5, 10.5)
# CSPlot.set_xlabel('Displacement (cm)')
# CSPlot.set_ylabel('Force (N)')
#
# CLPlot.clear()
# CLPlot.plot(dispCL, phal1DataCL, 'o')
# CLPlot.plot(dispCL, phal2DataCL, 'o')
# CLPlot.set_ylim(-0.5, 10.5)
# # CLPlot.set_xlim(-0.5, 10.5)
# CLPlot.set_xlabel('Displacement (cm)')
# CLPlot.set_ylabel('Force (N)')

# C0Plot.title.set_text('0 Offset')
# CSPlot.title.set_text('Small Offset')
# CLPlot.title.set_text('Large Offset')

# plt.draw()
plt.show()

