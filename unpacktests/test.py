# coding: utf-8

from binascii import *

from taobaotmcpy.messageio import reader

s = '020205002400000035363630303062392d626538382d343465612d383431632d6132613865333565373964300100060000005f5f6b696e640101000000310000'

message = reader(unhexlify(s))
print(message.token)
print(message.content)

_MAX_INTEGER = (1 << 32) - 1
_MAX_LONG = (1 << 64) - 1
_AVAILABLE_KEY_CHARS = list(range(0x21, 0x2f + 1)) + list(range(0x3a, 0x7e + 1))
_MAX_CHAR_BYTE = (1 << 8) - 1

print(_MAX_INTEGER)
print(_MAX_LONG)
print(_AVAILABLE_KEY_CHARS)
print(_MAX_CHAR_BYTE)
