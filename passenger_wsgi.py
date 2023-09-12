import os
import sys
import imp


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'core/wsgi.py')
application = wsgi.application
