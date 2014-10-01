Performance Logging
=========

Record JMX values from a running Cassandra process, using JMXTerm (http://wiki.cyclopsgroup.org/jmxterm/), and do the following:

* Put the records into a Cassandra table.
* Plot the results.

Based on a Cassandra question on Glassdoor.

Currently, the first version only works on Windows (DataStax Community installer). Developed and tested in Python 2.7.

## Input/Output

**Input**

If running the script from command line, the following arguments must be provided:

* installDir INSTALLDIR:  Path to installation directory.
* host HOST            :  URL string for Cassandra instance. Only localhost tested.
* jmxTerm JMXTERM      :  Path to jmxterm jar file.
* osString OSSTRING    :  String that represents the current OS. Windows: win. Mac: mac. Unix/Linux: linux.

Example:
python PerformanceLog.py -installDir C:\datastax -host localhost -jmxTerm lib\jmxterm.jar -osString win

** Output **

* CSV file

Example:
>	SSTableCount,DataSize,c95thPercentile
>	0,0,0.0
>	7,31306299,9337.784849999995
	7,31306299,9262.307649999999
	7,46377363,9981.513249999998
	8,43848053,6715.435949999997
	9,59332534,6299.833299999999
	10,71433598,6165.590649999999
	11,71034536,6406.8352499999955
	12,68976063,6517.250999999998
	13,49334620,6565.55335
	14,47699160,6495.163199999996
	15,56378325,6490.254449999997
	12,94854827,6331.381099999998
	13,92410210,6458.84175

* Performance plot (based on CSV output) as PNG file

Example:

![alt text](https://dl.dropbox.com/s/0vy2u8b7hb7djjv/jmxMetrics.png "Performance Plot")


## Python modules
1. PerformanceLog.py: Main module to run the automated tasks. Please use "python DataStax -h"
for the required arguments. Example call for Windows is in the doc string.
2. MyLogger.py: Logging support module
3. CassandraRecord.py: Support module to record metrics into a Cassandra table.
4. Plotter.py: Support module to plot metrics into plots and save into PNG file.

### Automated tasks by the modules
1. Check if Cassandra is Running
2. Record certain JMX Metrics 
3. Runs the external tool Cassandra Stress
4. Once the stress session has completed, stop recording JMX Metrics
5. Record the metrics back into a Cassandra Table
6. Graph the results (create these graphs at the end of the run).

## External Python libraries required

#### For CassandraRecord.py

This module requires Datastax's Python driver: http://datastax.github.io/python-driver/installation.html

#### For Plotter.py

This Python module used Matplotlib library. Please install the following Python libraries: matplotlib, numpy, dateutil, pytz, pyparsing, six. (optionally pillow, pycairo, tornado, wxpython, pyside, pyqt, ghostscript, miktex, ffmpeg, mencoder, avconv, or imagemagick)

Installation of these Python libraries are straight-forward on Linux and Win32. On Win64, please find installers here: http://www.lfd.uci.edu/~gohlke/pythonlibs/


## Other files

The following output files are produced. For consistency check, they are left behind.
In the final version of the script, they may be cleaned up accordingly.

* tempout: Output from JmxTerm session
* jmxMetrics.csv: The cvs file that records the interested JMX metrics.
* CassandraTest.log: The log file for the script.
