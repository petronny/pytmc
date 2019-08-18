# coding: utf-8
__author__ = 'baocaixiong'

import logging

from tornado import ioloop
from tornado.options import parse_command_line

from .tmcclient import TmcClient


if __name__ == '__main__':
    cli = parse_command_line()

    logging.basicConfig(level=logging.DEBUG)
    ws = TmcClient('ws://mc.api.taobao.com/', 'app_key', 'app_secret', 'default',
                   query_message_interval=50)

    def print1():
        print('on_open')

    ws.on("on_open", print1)

    try:
        ioloop.IOLoop.current().run_sync(ws.start)
    except KeyboardInterrupt:
        pass
    finally:
        ioloop.IOLoop.current().run_sync(ws.close)
