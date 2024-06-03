from pprint import pprint
from server import Server
from config import token
server1 = Server(token, 226103931, "server1")
try:
    server1.start()
except Exception as _ex:
    pprint(_ex)