from json import dumps

class MessageType(object):

    CONNECT = 0
    CONNECTACK = 1
    SEND = 2
    SENDACK = 3

    class HeaderType(object):
        endOfHeaders = 0
        custom = 1
        statusCode = 2
        statusPhrase = 3
        flag = 4
        token = 5

    class ValueFormat(object):
        void = 0
        countedString = 1
        byte = 2
        int16 = 3
        int32 = 4
        int64 = 5
        date = 6
        byteArray = 7

class Message(object):

    def __init__(self, protocol_version=2, message_type=None, status_code=None,
                 status_phrase=None, flag=None, token=None, content=None):
        self.protocol_version = protocol_version
        self.message_type = message_type
        self.status_code = status_code
        self.status_phrase = status_phrase
        self.flag = flag
        self.token = token
        self.content = content if content is not None and isinstance(content, dict) else {}
        self.offset = 0

    def update_offset(self, offset):
        self.offset = self.offset + offset

        return self

    def __str__(self):
        return dumps(self.__dict__, ensure_ascii=False)

    __repr__ = __str__

class ConfirmMessage(Message):

    def __init__(self, message_id, token):
        content = {'__kind': 2, 'id': message_id}
        super().__init__(message_type=2, token=token, content=content)

class QueryMessage(Message):

    def __init__(self, token):
        content = {'__kind': 1}
        super().__init__(message_type=2, token=token, content=content)
