# NosCrypto
A reverse engineered packet cryptography - encryption and decryption routines to emulate NosTale client or server.

# Abstract
The goal of this project is to recreate an algorithm that is used to encrypt/decrypt net packets that are exchanged between NosTale client and server. I've seen many public cryptos but I think none of them were producing exactly the same output as real client or server (especially when it comes to special characters like `ąśżź` etc). The problem of a majority of those libraries is an incorrect mask generation algorithm. If you ever encounter output produced by this library that is different from the original produced by game client or server, please report it immediately.

# Installation 
Please use pypi to install this library:

`pip install noscrypto`

# Tests
Unit tests are available under `noscrypto/tests`

# Usage
All the functions accept `bytes` as input and return `bytes` as output. Keep in mind that each function should accept and output only single packet. It is extremely important when you are, for example decrypting world packets as a client, because sometime the server sends multiple packets in one call (they are splited by 0xFF, and you should decrypt the packets chunk by chunk) 

## Client
Functions can be imported like
```python
from noscrypto import Client
```

### Client.LoginEncrypt
Encrypts your packet so the login server can read it. Automatically adds the `\n` character at the end of packet if not present.

```python
>>> Client.LoginEncrypt("hey".encode("ascii"))
b'\xba\xb5\xc9\xd8'
```

### Client.LoginDecrypt
Decrypts your login result packet, so you can read it

```python
>>> Client.LoginDecrypt(b'\x75\x70\x78\x7B\x72\x2F\x44\x19').decode("ascii")
'failc 5\n'
```

### Client.WorldEncrypt
Encrypts your pakcet so the world server can read it. Beside `packet` you also need to supply your `session` (that one you received from login server). The last parameter `is_first_packet` (default `False`) must be set to `True` only if you are sending your first packet to the world server (the session packet)

```python
>>> Client.WorldEncrypt("hey!".encode("ascii"), 1337, False)
b'}\x10\x13\xffWx'
```

### Client.WorldDecrypt
Decrypts your wolrd packet sent by server, so you can read it

```python
>>> Client.WorldDecrypt(b'\x04\x8C\x8B\x9E\x8B\x96\x16\x65\x16\x65\x1A\x41\xA4\x14\x15\x46\x8E\xFF')
b'stat 221 221 60 60 0 1024\n'
```

### Client.WorldDecryptList
Decrypts your world packets sent by server like Client.WorldDecrypt, but return list of this packets.
Nostale server sometimes send more packets one time

```python
>>> recvByte = b'\r\x9c\x93\x96\x8c\x8b\xa0\x8c\x8b\x9e\x8d\x8b\xdf\xcf\xff~\x9c\x93\x96\x8c\x8b\xdf\xcf\xdf\xb4\x96\x93\x93\x8d\x90\x98\xdf\xcf\xdf\xcf\xdf\xce\xdf\xc8\xdf\xcf\xdf\xcd\xdf\xc6\xc6\xdf\xce\xdf\xd2\xce\xd1\xcd\xc6\xca\xd1\xcc\xcb\xd1\xcd\xc7\xc6\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xdf\xc7\xcf\xdf\xdf\xce\xdf\xce\xdf\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\x16\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xd1\xd2\xce\xdf\xcf\xdf\xcf\xff\t\x9c\x93\x96\x8c\x8b\xa0\x9a\x91\x9b\xff'
>>> WorldDecryptList(recvByte, encoding="ascii")
['clist_start 0', 'clist 0 Killrog 0 0 1 7 0 2 99 1 -1.295.34.289.-1.-1.-1.-1 80  1 1 -1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1 0 0', 'clist_end']
```

## Server
Functions can be imported like
```python
from noscrypto import Server
```

### Server.LoginEncrypt
Encrypts your packet so the client can read it. Automatically adds the `\n` character at the end of packet if not present.
```python
>>> Server.LoginEncrypt("hello world".encode("ascii"))
b'wt{{~/\x86~\x81{s\x19'
```

### Server.LoginDecrypt
Decrypts login packet from client, so you can read it
```python
>>> Server.LoginDecrypt(b'\xba\xb5\xc9\xd8').decode("ascii")
'hey\n'
```

### Server.WorldEncrypt
Encrypt world packet, so the client can read it
```python
>>> Server.WorldEncrypt("stat 221 221 60 60 0 1024\n".encode("ascii"))
b'\x04\x8c\x8b\x9e\x8b\x96\x16e\x16e\x1aA\xa4\x14\x15F\x8e\xff'
```
### Server.WorldDecrypt
Decrypts client pakcet so the world server can read it. Beside `packet` you also need to supply client `session`. The last parameter `is_first_packet` (default `False`) must be set to `True` only if you didn't recv the first packet from client yet (the session packet).

```python
>>> Server.WorldDecrypt(b'}\x10\x13\xffWx', 1337, False).decode("ascii")
'hey!'
```
