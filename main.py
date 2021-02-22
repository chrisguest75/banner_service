#!/usr/bin/env python3
"""
A skeleton OpenApi v2 interface and service.  Useful for using with Google Endpoints. 
"""

import argparse
import io
import logging
import logging.config
import os
import sys
import traceback

import yaml

import ptvsd


def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.critical("Exception", exc_info=(
        exc_type, exc_value, exc_traceback))
    logging.critical('Unhandled Exception {0}: {1}'.format(exc_type, exc_value), extra={
                     'exception': ''.join(traceback.format_tb(exc_traceback))})


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


if __name__ == "__main__":
    print(f"Enter {__name__}")
    with io.open("./logging_config.yaml") as f:
        logging_config = yaml.load(f, Loader=yaml.SafeLoader)

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger()

    sys.excepthook = log_uncaught_exceptions

    parser = argparse.ArgumentParser(description='Wordament Solver Service')
    parser.add_argument('--debugger', dest='debugger', action='store_true')
    parser.add_argument('--wait', dest='wait', action='store_true')
    args = parser.parse_args()

    debugger = False
    if 'DEBUGGER' in os.environ:
        debugger = str2bool(os.environ['DEBUGGER'])
        logger.info(f"DEBUGGER found in environment {debugger}", extra={
                    "debugger": debugger})
    if args.debugger:
        debugger = True

    wait = False
    if 'WAIT' in os.environ:
        wait = str2bool(os.environ['WAIT'])
        logger.info(f"WAIT found in environment {wait}", extra={"wait": wait})
    if args.wait:
        wait = True

    if debugger:
        # 5678 is the default attach port in the VS Code debug configurations
        print("Debugger activated")
        ptvsd.enable_attach(address=('0.0.0.0', 5678), redirect_output=True)
        if wait:
            logger.info("Waiting for debugger attach")
            ptvsd.wait_for_attach()
            breakpoint()

    server_port = os.environ.get('PORT')
    if server_port is None:
        logger.error(f"PORT environment variable not set")
        exit(1)

    from app import app, home
    app.run(port=server_port, host='0.0.0.0', use_reloader=False)

    exit(0)
