import time
from hashlib import md5
import logging
import asyncio
import websockets
from .messageio import reader, writer
from .message import Message, ConfirmMessage, QueryMessage

logger = logging.getLogger('pytmc')

class Protocol(websockets.WebSocketClientProtocol):

    #async def ping(self, data=None):
    #    logger.debug('recv ping')
    #    pong = await super().ping(data=data)
    #    await pong

    #async def pong(self, data=b''):
    #    logger.debug('send pong')
    #    await super().pong(data)

    async def recv(self):
        message = await super().recv()
        message = reader(message)
        logger.debug('recv %s' % message)
        return message

    async def send(self, message):
        logger.debug('send %s' % message)
        await super().send(writer(message))

    #async def wait_closed(self):
    #    logger.debug('on_wait_closed')
    #    await super().close()

    #async def close(self, code=1000, reason=''):
    #    logger.debug('on_close')
    #    await super().close(code=code, reason=reason)

class Client:

    #sdk='top-sdk-java-20180730'
    sdk = 'pytmc-20190819'

    def __init__(self, url='ws://mc.api.taobao.com/', app_key=None, app_secret=None, group='default', protocol=Protocol, query_message_interval=50):
        self.url = url
        self.app_key = app_key
        self.app_secret = app_secret
        self.group = group
        self.protocol = protocol
        self.query_message_interval = query_message_interval

    async def on_start(self):
        pass

    async def on_open(self):
        pass

    async def on_message(self, message):
        pass

    async def on_close(self):
        pass

    def __get_signature__(self, timestamp):
        timestamp = timestamp if timestamp else int(round(time.time() * 1000))
        params = {
                'group_name': self.group,
                'app_key': self.app_key,
                'timestamp': timestamp,
        }
        keys = list(params.keys())
        keys.sort()
        params = "%s%s%s" % (self.app_secret, str().join('%s%s' % (key, params[key]) for key in keys), self.app_secret)
        return md5(params.encode('utf-8')).hexdigest().upper()

    async def __on_start__(self):
        logger.info('Websocket start connect: %s@%s' % (self.url, self.group))
        await self.on_start()

    async def __on_open__(self):
        timestamp = int(round(time.time() * 1000))
        logger.info('[%s] TMC handshake start.' % self.group)

        params = {
                'timestamp': str(timestamp),
                'app_key': self.app_key,
                'sdk': Client.sdk,
                'sign': self.__get_signature__(timestamp),
                'group_name': self.group,
        }

        message = Message(message_type=0, flag=1, content=params)
        await self.websocket.send(message)
        await self.on_open()

    async def __on_message__(self, message):
        if message.message_type == 1:
            self.token = message.token
            if self.token:
                logger.info('[%s] TMC handshake success. The token is %s' % (self.group, message.token))
                await self.__on_handshake_success__(self.token)
            else:
                logger.info('[%s] TMC handshake failed. Error: %s' % (self.group, message))
        elif message.message_type == 2:
            await self.__confirm_message__(message_id=message.content.get('id'))
            await self.on_message(message)
        elif message.message_type == 3:
            logger.info(message)

    async def __on_handshake_success__(self, token):
        logger.info('[%s] Start query message.' % self.group)
        while True:
            try:
                message = await asyncio.wait_for(self.websocket.recv(), timeout=self.query_message_interval)
                await self.__on_message__(message)
            except asyncio.TimeoutError:
                await self.websocket.send(QueryMessage(self.token))

    async def __confirm_message__(self, message_id):
        message = ConfirmMessage(message_id, self.token)
        await self.websocket.send(message)
        logger.debug('[%s] Confirmed message %s.' % (self.group, message_id))

    async def __on_close__(self):
        logger.error('[%s] TMC connection closed.' % self.group)
        await self.on_close()

    async def start(self):
        await self.__on_start__()

        async with websockets.connect(self.url, create_protocol=self.protocol) as self.websocket:
            await self.__on_open__()
            message = await self.websocket.recv()
            await self.__on_message__(message)

        await self.__on_close__()
