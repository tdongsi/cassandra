'''
Created on Sep 30, 2014

My plotting module.

@author: tdongsi
'''

import matplotlib.pyplot as plt
import numpy as np
import MyLogger
import logging

# create logger
myLogger = logging.getLogger('Plotter')

def parseCsv(csvFile):
    '''
    Parsing a simple CSV file.
    The first line is comma-separated header strings.
    The following lines are decimal numbers for data.
    
    Input:
    csvFile: string represents file path and name to the CSV file
    Output:
    headerList: list of header strings
    dataList: list of lists, for each data list corresponding to each header. 
    '''
    try:
        with open( csvFile, "r" ) as f:
            lines = f.readlines()
        
        headerList = lines[0].split(',')
        
        # Initialize list of lists
        dataList = [[] for x in range(len(headerList))]
        for line in lines[1:]:
            numbers = line.split(',')
            for i in range(len(numbers)):
                dataList[i].append(float(numbers[i]))
        
        return headerList, dataList
    except IOError:
        myLogger.error( 'Error opening file %s', csvFile )
    
    # Only here in error cases
    return None, None

def plotCsv(csvFile, pngFile, customHeaders = None):
    '''
    Get in a csvFile and generate plots as pngFile.
    '''
    (headerList, dataList) = parseCsv(csvFile)
    # due to possible long header strings, use custom headers
    if customHeaders and len(customHeaders) == len(headerList):
        headerList = customHeaders
    
    myLogger.debug(headerList)
    for i in range(len(headerList)):
        myLogger.debug(dataList[i])

    plotNum = len(headerList)
    # Another one for legends
    figure, plots = plt.subplots(plotNum, 1, True )
    # Adjust this number so that the ylabels of the subplots are aligned
    labelx = -0.1
    
    # Some pre-defined colors and styles for the subplots
    colors = ['bo-', 'g*-', 'rs-', 'c8-', 'm<-', 'kv-']
    # if the number of plots is larger, expand colors accordingly
    for i in range(len(colors), plotNum):
        colors[i] = 'kv-'
    
    
    for idx in range(len(headerList)):
        matrix = np.array(dataList[idx])
        plots[idx].plot(matrix[:], colors[idx])
        plots[idx].set_ylabel( headerList[idx])
        
        # Extra settings
        plots[idx].yaxis.set_label_coords(labelx, 0.5)
        plots[idx].grid(True)
    
    plt.xlabel('Check points')
    plt.savefig(pngFile, dpi = 300, bbox_inches='tight' )
    # DEBUG: enable this if you want to see the plot
    plt.show()

def main():
    plotCsv('jmxMetrics.csv', 'jmxMetrics.png')

if __name__ == "__main__":
    ''' Usage: See the top comment for usage of this module.'''
    print 'Running the script'
    
    main()

