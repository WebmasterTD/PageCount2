#/bin/bash
gunicorn --worker-class gevent --timeout 90  --bind 0.0.0.0:8000 wsgi --workers 2
