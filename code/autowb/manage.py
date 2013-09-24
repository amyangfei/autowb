#!/usr/bin/env python
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, ROOT_DIR + '/code')
sys.path.insert(0, ROOT_DIR + '/code/autowb')


# import SocketServer
# import django.core.servers.basehttp
# django.core.servers.basehttp.WSGIServer = \
#     type('WSGIServer',
#          (SocketServer.ThreadingMixIn,
#           django.core.servers.basehttp.WSGIServer,
#           object),
#          {})
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
