import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import random
from conference import Conference
from person import Person


class Server:

    def __init__(self, api_token, group_id, server_name: str = "Empty"):
        # Даем серверу имя
        self.server_name = server_name
        # Для Long Poll
        self.vk = vk_api.VkApi(token=api_token)

        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk, group_id)

        # Для вызова методов vk_api
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message):
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=random.randint(0, 6000))

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        self.send_msg(384407860, "Привет-привет!")

    def start(self):
        for event in self.long_poll.listen():  # Слушаем сервер
            if event.type == VkBotEventType.MESSAGE_NEW:
                print(event.message)
                if "/" in event.message['text']:
                    self.command(event.message)
                if 'action' in event.message:
                    self.action(event.message)

    def command(self, message):
        conf = Conference(message['peer_id'] - 2000000000)  # получение информации о конфе в которой написали команду
        initiator = Person(message['from_id'])
        if "/test" in message['text']:
            self.send_msg(message['peer_id'], f"Бот работает!")
        if "/kick" in message['text']:
            for i in range(len(initiator.conference)):
                if (initiator.rang[i] >= 1) and (initiator.conference[i] == message['peer_id'] - 2000000000):
                    self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                        member_id=int(message['text'][5:].split("|")[0].replace("[id", "")))
                    self.send_msg(message['peer_id'],
                                  f"{initiator.nick[i]} кикнул {message['text'][5:].split('|')[1].replace(']','')}")
                else:
                    self.send_msg(message['peer_id'], "Недостаточно прав")
                break
        if "/hi" in message['text']:
            conf.setHi(message['text'][3:])
            self.send_msg(message['peer_id'], f"Приветственное сообщение задано!")

    def action(self, message):
        conf = Conference(message['peer_id'] - 2000000000)  # получение информации о конфе в которой написали команду
        # приветственное сообщение при инвайте нового пользователя
        if message['action']['type'] == 'chat_invite_user':
            self.send_msg(message['peer_id'], conf.hi)
        # кик игрока, который вышел
        if message['from_id'] == message['action']['member_id'] and message['action']['type'] == 'chat_kick_user':
            self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                member_id=int(message['from_id']))
