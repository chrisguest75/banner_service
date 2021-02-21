# flask_request_intercepts.py
#
# This class and methods are used to intercept calls and log before the user handler is invoked.

import logging
from flask import g, Flask, request, jsonify
import traceback
from werkzeug.exceptions import HTTPException, NotFound
from flask import got_request_exception
import time

logger = logging.getLogger('app.flask.intercepts')


class flask_intercepts():
    def __init__(self, app):
        app = app.app
        app.before_request(flask_intercepts.before_request)
        app.after_request(flask_intercepts.after_request)
        # got_request_exception.connect(FlaskRequestIntercepts.log_exception, self.app)

    @staticmethod
    def before_request():
        g.start = time.time()

        log_extra = {'remote_address': request.remote_addr,
                     'method': request.method.lower(),
                     'scheme': request.scheme,
                     'full_path': request.full_path
                     }

        logger.debug('Request from "{0}" to {2} "{1}"'.format(
            request.remote_addr, request.full_path, request.method.lower()), extra=log_extra)

    @staticmethod
    def after_request(response):
        #     if request.path == '/favicon.ico':
        #         return response
        #     elif request.path.startswith('/static'):
        #         return response

        now = time.time()
        duration = round(now - g.start, 2)
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host.split(':', 1)[0]
        args = dict(request.args)

        log_extra = {'remote_address': request.remote_addr,
                     'ip': ip,
                     'host': host,
                     'params': args,
                     'method': request.method.lower(),
                     'scheme': request.scheme,
                     'full_path': request.full_path,
                     'status': response.status,
                     'status_code': response.status_code,
                     'duration': duration}

        request_id = request.headers.get('X-Request-ID')
        if request_id:
            log_extra['request_id'] = request_id

        # this if avoids the duplication of registry in the log,
        # since that 500 is already logged via @app.errorhandler
        if response.status_code != 500:
            logger.info('{3} response to request from "{0}" to {2} "{1}"'.format(
                request.remote_addr, request.full_path, request.method.lower(), response.status), extra=log_extra)
        else:
            log_extra['response_payload'] = response.response
            logger.error('{3} response to request from "{0}" to {2} "{1}"'.format(
                request.remote_addr, request.full_path, request.method.lower(), response.status), extra=log_extra)

        return response

    @staticmethod
    def log_exception(sender, exception, **extra):
        # an uncaught exception will always be 500
        logger = logging.getLogger(__name__)
        tb = traceback.format_exc()
        logger.error({'message': 'Exception during response to request from "{0}" to {2} "{1}"'.format(request.remote_addr, request.full_path, request.method.lower()),
                      'remote_address': request.remote_addr,
                      'method': request.method.lower(),
                      'scheme': request.scheme,
                      'full_path': request.full_path,
                      'stacktrace': tb,
                      'status_code': 500
                      })
