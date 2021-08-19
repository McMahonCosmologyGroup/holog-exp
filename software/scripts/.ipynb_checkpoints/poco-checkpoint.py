'''
Functions for operating the Casper ROACH2 FPGA.
Grace E. Chesmore
July 19, 2021
'''
import logging
import sys

def exit_fail(fpga,l_handler):
    """Exit and print failure statement."""
    print('FAILURE DETECTED. Log entries:\n',l_handler.printMessages())
    try:
        fpga.stop()
    except:
        pass
    sys.exit()

def exit_clean(fpga):
    """Exit and clean FPGA."""
    try:
        fpga.stop()
    except:
        pass
    sys.exit()

 # debug log handler
class DebugLogHandler(logging.Handler):
    """A logger for KATCP tests."""

    def __init__(self,max_len=100):
        """Create a TestLogHandler.
            @param max_len Integer: The maximum number of log entries
                                    to store. After this, will wrap.
        """
        logging.Handler.__init__(self)
        self._max_len = max_len
        self._records = []

    def emit(self, record):
        """Handle the arrival of a log message."""
        if len(self._records) >= self._max_len:
            self._records.pop(0)
        self._records.append(record)

    def clear(self):
        """Clear the list of remembered logs."""
        self._records = []

    def set_max_len(self,max_len):
        """The maximum number of log entries to store.
            After this, will wrap."""
        self._max_len=max_len

    def print_messages(self):
        """Printing in cases of ERROR."""
        for i in self._records:
            if i.exc_info:
                print('%s: %s Exception: '%(i.name,i.msg),i.exc_info[0:-1])
            else:
                if i.levelno < logging.WARNING:
                    print('%s: %s'%(i.name,i.msg))
                elif (i.levelno >= logging.WARNING) and (i.levelno < logging.ERROR):
                    print('%s: %s'%(i.name,i.msg))
                elif i.levelno >= logging.ERROR:
                    print('%s: %s'%(i.name,i.msg))
                else:
                    print('%s: %s'%(i.name,i.msg))