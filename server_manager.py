from server import Server
from config import token
server1 = Server(token, 226103931, "server1")
def main():
    try:
        server1.start()
    except Exception as _ex:
        print(_ex)
        main()


main()




