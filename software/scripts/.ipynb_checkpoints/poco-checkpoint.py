import sys
import logging

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
        if len(self._records) >= self._max_len: self._records.pop(0)
        self._records.append(record)

    def clear(self):
        """Clear the list of remembered logs."""
        self._records = []

    def setMaxLen(self,max_len):
        self._max_len=max_len

    def printMessages(self):
        for i in self._records:
            if i.exc_info:
                print '%s: %s Exception: '%(i.name,i.msg),i.exc_info[0:-1]
            else:
                if i.levelno < logging.WARNING:
                    print '%s: %s'%(i.name,i.msg)
                elif (i.levelno >= logging.WARNING) and (i.levelno < logging.ERROR):
                    print '%s: %s'%(i.name,i.msg)
                elif i.levelno >= logging.ERROR:
                    print '%s: %s'%(i.name,i.msg)
                else:
                    print '%s: %s'%(i.name,i.msg)
