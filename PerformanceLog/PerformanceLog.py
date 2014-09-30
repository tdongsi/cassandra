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
import argparse
import os
import subprocess
import threading
import time

# create logger
myLogger = logging.getLogger('Installer')

class JmxLogger(object):
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
            # cassandra-stress in installDir\apache-cassandra\tools\bin
            self._stresstool = os.path.join(self._installDir, 'apache-cassandra', 
                                'tools', 'bin', 'cassandra-stress.bat')
        else:
            # TODO
            pass
    
    def run(self):
        if self.isCassandraRunning():
            myLogger.info( 'An running Cassandra instance is found')
            
            myThread = threading.Thread(target = self.runCassandraStress)
            myThread.start()
            
            count = 0
            while True:
                time.sleep(2)
                count += 1
                self.logJmx(count)
                
                if not myThread.isAlive():
                    break
                
            myLogger.info( 'Finish logging JMX metrics')
            
        else:
            myLogger.error( 'Cassandra instance is not found running')
            
    def logJmx(self, count):
        print count
        return
    
    def runCassandraStress(self):
        '''
        3. Runs the external tool Cassandra Stress.
        '''
        # Sleep 5 seconds to wait for JMX logging 
        time.sleep(5)
        
        myLogger.debug( '> %s', self._stresstool)
        try:
            output = subprocess.check_output( self._stresstool, stderr=subprocess.STDOUT )
            myLogger.debug("%s" % output)
        except subprocess.CalledProcessError as e:
            myLogger.error( "Error code: %d" % e.returncode)
            myLogger.error(e.output)
            
        time.sleep(5)
    
    
    def isCassandraRunning(self):
        '''
        1. Check if Cassandra is running
        By running: nodetool -host host version
        Naive way:
        If it is running, the environment variable %errorlevel% is 0.
        Otherwise, the error level is non-zero, usually 1.
        
        In practice, the batch script returns 0, even with wrapper runWinBatch.
        Instead, we perform text matching to confirm Cassandra running.
        '''
        
        cmdStr = [self._nodetool, '-host', self._host, 'version']
        myLogger.debug( '> %s', ' '.join(cmdStr))
        try:
            output = subprocess.check_output( cmdStr, stderr=subprocess.STDOUT )
            myLogger.debug("%s" % output)
            
            if 'ReleaseVersion' in output:
                return True
            else:
                return False
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
    
    jmxLogger = JmxLogger(args.installDir, args.host, args.jmxTerm, args.osString)
    jmxLogger.run()
    

if __name__ == "__main__":
    ''' Usage: See the top comment for usage of this script.'''
    print 'Running the script'
    out = main()
