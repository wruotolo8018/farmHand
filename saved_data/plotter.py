import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

"""
plotData

Takes in a numpy array and plots the collected data for the user to visualize.

Arguments:
    dataArray -- A numpy array that contains the data streams and time

Returns:None

"""

def plotData(dataArray):

    style.use('fivethirtyeight')
    fig, mainPlot = plt.subplots(nrows=1,ncols=1)

    print("dataArray.shape: " + str(dataArray.shape))

    try:
        plotArrayFloat = np.array([[float(x) for x in y] for y in dataArray])

        #time = plotArrayFloat[2,:]

        data_1 = plotArrayFloat[0,:]
        data_2 = plotArrayFloat[1,:]
        z_pos = plotArrayFloat[2,:]

        mainPlot.clear()
        mainPlot.plot(z_pos, data_1, 'o', color='green')
        mainPlot.plot(z_pos, data_2, 'o', color = 'black')

	#mainPlot.plot(data_1)
        #mainPlot.plot(data_2)

        mainPlot.title.set_text('Current Data')

        plt.draw()
        plt.show()

    except:
        print("Failed to Generate Plot")
