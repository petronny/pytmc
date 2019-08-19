import json
import asyncio
import logging
from tornado.log import enable_pretty_logging
from tornado.options import options
options.logging = 'info'
logger = logging.getLogger('pytmc')
enable_pretty_logging(options=options, logger=logger)

from .client import Client

if __name__ == '__main__':

    class MyClient(Client):

        async def on_start(self):
            pass

        async def on_open(self):
            pass

        async def on_message(self, message):
            log = []
            content = json.loads(message.content['content'])
            log.append(message.content['time'])
            log.append(message.content['nick'])
            logger.info('\t'.join([str(i) for i in log]))

        async def on_close(self):
            pass

    client = MyClient(app_key='app_key', app_secret='app_secret', group='default')
    asyncio.get_event_loop().run_until_complete(client.start())
