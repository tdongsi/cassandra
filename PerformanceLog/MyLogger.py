'''
Created on Sep 29, 2014

My logging configuration.

@author: tdongsi
'''

import logging
import subprocess
import inspect

# set up logging to file
LOG_FILENAME = 'CassandraTest.log'
# Additional logging info: %(asctime)s %(name)-12s 
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s {%(name)-12s} %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILENAME,
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

def runWinBatch(logger, cmdStr):
    '''
    Run the batch file and return the error level.
    There is little correlation between process exit code and the errorlevel 
    environment variable when running batch script in Windows.
    This method provides a wrapper for the Windows batch scripts that
    returns the correct error level. 
    '''
    
    # Print out the caller module and its line number
    logger.debug( 'Calling from %s' % str(inspect.stack()[1][1:3]))
    # run a command without exiting
    winCmd = ['cmd', '/K']
    winCmd.extend(cmdStr)
    logger.debug( '> %s', ' '.join(winCmd))
    
    p = subprocess.Popen(winCmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate(r'exit %errorlevel%\r\n')
    
    return p.returncode
    

def runCommand(logger, cmdStr):
    # Print out the caller module and its line number
    logger.debug( 'Calling from %s' % str(inspect.stack()[1][1:3]))
    logger.info( '> %s', ' '.join(cmdStr))
    try:
        output = subprocess.check_output( cmdStr, stderr=subprocess.STDOUT )
        logger.debug(output)
    except subprocess.CalledProcessError as e:
        logger.error( "Error code: %d" % e.returncode)
        logger.error(e.output)
        
        
if __name__ == "__main__":
    print "My configured logging module."
    
