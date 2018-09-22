### taobao-tmc-python

淘宝平台消息服务python版本

#### Usage
```python
import taobaotmcpy
import tornado
import logging

logging.basicConfig(level=logging.DEBUG)

ws = taobaotmcpy.TmcClient('ws://mc.api.tbsandbox.com/', 'appkey', 'appsecret', 'default',
    query_message_interval=50)

def on_open():
    print('on_open')

def on_message(message):
    print('on_message')
    print(message)

def on_ping():
    print('on_ping')

def on_pong():
    print('on_pong')

def on_close():
    print('on_close')

ws.on("on_open", on_open)
ws.on("on_message", on_message)
ws.on("on_ping", on_ping)
ws.on("on_pong", on_pong)
ws.on("on_close", on_close)

try:
    tornado.ioloop.IOLoop.instance().start()
except KeyboardInterrupt:
    pass
finally:
    ws.close()
```
