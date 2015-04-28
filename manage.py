#!/usr/bin/env python
import os
import sys

# Taken from: http://stackoverflow.com/a/15649485/118608
# Monkeypatch python not to print "Broken Pipe" errors to stdout.
import socketserver
from wsgiref import handlers
def handle_err(self, request, client_address):
    """Handle an error gracefully.  May be overridden.

    The default is to print a traceback and continue.

    """
    # print("handle_error() hit")
    import traceback
    if 'BrokenPipeError' in traceback.format_exc():
        pass
    else:
        print('-'*40)
        print('Exception happened during processing of request from', end=' ')
        print(client_address)
        print(traceback)
        print('-'*40)
socketserver.BaseServer.handle_error = handle_err

def log_exc(self,exc_info):
    """Log the 'exc_info' tuple in the server log

    Subclasses may override to retarget the output or change its format.
    """
    # print("log_exception() hit")
    # print('exc_info[0] = %s' % exc_info[0])
    # print('exc_info[1] = %s' % exc_info[1])
    # print('exc_info[2] = %s' % exc_info[2])

    if exc_info[0] is BrokenPipeError: # (BrokenPipeError, ConnectionResetError)):
        exc_info = None
        return

    try:
        from traceback import print_exception
        stderr = self.get_stderr()
        print_exception(
            exc_info[0], exc_info[1], exc_info[2],
            self.traceback_limit, stderr
        )
        stderr.flush()
    finally:
        exc_info = None

handlers.BaseHandler.log_exception = log_exc

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "global_change_lab.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
