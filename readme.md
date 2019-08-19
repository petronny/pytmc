pytmc
====
淘宝平台消息服务 Python Websocket 客户端


### 依赖
* Python 3.6+
* [python-websockets](https://pypi.org/project/websockets/)


### Usage

* 继承 `pytmc.Client` 类并按需重载 `on_start()`, `on_open()`, `on_message()` 等事件函数

```
from pytmc import Client

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
```

* 使用 `asyncio` 启动子类实例中的 `start()` 函数

```
client = MyClient(app_key='app_key', app_secret='app_secret', group='default')
asyncio.get_event_loop().run_until_complete(client.start())
```
