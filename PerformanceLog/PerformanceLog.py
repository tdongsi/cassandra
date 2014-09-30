'''
Created on Sep 29, 2014

DataStax exercise

Usage:

Example:
python DataStax.py -installDir C:\datastax -host localhost -jmxTerm lib\jmxterm.jar -osString win

@author: tdongsi
'''

import logging
import MyLogger
from MyLogger import runCommand
import argparse
import os
import subprocess

# create logger
myLogger = logging.getLogger('Installer')

class JmxLogger:
    def __init__(self, installDir, host, jmxTerm, osString = 'win'):
        self._installDir = installDir
        self._host = host
        self._jmxTerm = jmxTerm
        self._osString = osString
        
        if self._osString == 'win':
            # In Windows
            # nodetool in installDir\apache-cassandra\bin
            self._nodetool = os.path.join(self._installDir, 'apache-cassandra', 
                                          'bin', 'nodetool.bat')
        else:
            # TODO
            pass
    
    def run(self):
        if self.isCassandraRunning():
            myLogger.info( 'An running Cassandra instance is found')
        else:
            myLogger.error( 'Cassandra instance is not found running')
    
    def isCassandraRunning(self):
        '''
        1. Ensures Cassandra is running
        By running: nodetool -host host version
        Naive way:
        If it is running, the environment variable %errorlevel% is 0.
        Otherwise, the error level is non-zero, usually 1.
        '''
        
        cmdStr = [self._nodetool, '-host', self._host, 'version']
        myLogger.debug( '> %s', ' '.join(cmdStr))
        try:
            output = subprocess.check_output( cmdStr, stderr=subprocess.STDOUT )
            myLogger.debug("%s" % output)
            return True
        except subprocess.CalledProcessError as e:
            myLogger.error( "Error code: %d" % e.returncode)
            myLogger.error(e.output)
            return False
    

def main():
    '''Automate recording JMX values from a running Cassandra instance.'''
    
    parser = argparse.ArgumentParser(description='Script to automate running' 
        'Cassandra stress and recording JMX metrics.')
    
    parser.add_argument('-installDir', action='store', required=True,
                        dest='installDir', help='Path to installation directory.')
    
    parser.add_argument('-host', action='store', dest='host', 
                        required=True,
                        help='URL string for Cassandra instance. Only localhost tested.')
    
    parser.add_argument('-jmxTerm', action='store', dest='jmxTerm', 
                        required=True,
                        help='Path to jmxterm jar file.')
    
    parser.add_argument('-osString', action='store', dest='osString', 
                        required=True,
                        help='String that represents the current OS. '\
                        'Windows: win. '\
                        'Mac: mac. '\
                        'Unix/Linux: linux. ')    
    
    args = parser.parse_args()
    myLogger.debug( "Installation directory: %s", args.installDir )
    myLogger.debug( "URL of running instance: %s", args.host )
    myLogger.debug( "JmxTerm jar filepath: %s", args.jmxTerm )
    myLogger.debug( "Use-defined OS string: %s", args.osString)
    
    logger = JmxLogger(args.installDir, args.host, args.jmxTerm, args.osString)
    logger.run()
    

if __name__ == "__main__":
    '''
    Usage:
    
    '''
    print 'Running the script'
    out = main()
    print out