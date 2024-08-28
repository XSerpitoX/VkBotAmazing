from server import Server
from config import token

server1 = Server(token, 212389640, "server1")


def main():
    try:
        server1.start()
    except Exception as _ex:
        print(_ex)
        server1.send_msg(384407860, _ex)
        main()


if int(input('DEV mode: ')):
    server1.test()
    server1.start()
    #print(server1.get_info("celovekha")[0]['id'])
else:
    main()
