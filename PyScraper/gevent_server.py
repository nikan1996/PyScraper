#!/usr/bin/env python
# encoding: utf-8
"""

@author:nikan

@file: gevent_server.py

@time: 2018/6/19 上午10:19
"""

from gevent import monkey

monkey.patch_all()


from gevent.pywsgi import WSGIServer
import logging
import argparse

from PyScraper.server.app import create_app

logger = logging.getLogger(__name__)

app = create_app()


def init_args():
    parser = argparse.ArgumentParser(description='runtime api configures')
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        help='port for server',
                        default=5000)
    
    args = parser.parse_args()
    return args


def main():
    args = init_args()
    # gevent wsgi log reference
    # https://stackoverflow.com/questions/38063508/logging-with-wsgi-server-and-flask-application
    # app.run(host="0.0.0.0", port=args.port, debug=False)
    http_server = WSGIServer(('0.0.0.0', args.port), app, log=app.logger)
    http_server.serve_forever()


if __name__ == '__main__':
    main()
