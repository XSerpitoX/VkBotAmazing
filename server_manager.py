from pprint import pprint
from server import Server
from config import token
server1 = Server(token, 226103931, "server1")
def main():
    server1.start()


main()




