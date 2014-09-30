Performance Logging
=========

Record JMX values from a running Cassandra process, using JMXTerm (http://wiki.cyclopsgroup.org/jmxterm/), and do the following:

* Put the records into a Cassandra table.
* Plot the results.

Based on a Cassandra question on Glassdoor.

Currently, the first version only works on Windows (DataStax Community installer). Developed and tested in Python 2.7.


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
