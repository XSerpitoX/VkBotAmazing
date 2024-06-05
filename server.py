import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
import random
from conference import Conference
from person import PersonInitiator, PersonExperimental


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
        print(self.vk_api.users.get(user_ids="384407860", fields="screen_name"))

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
        initiator = PersonInitiator(message)
        if "/test" in message['text']:
            self.send_msg(message['peer_id'], f"Бот работает!")

        if "/kick" in message['text']:
            experimental = PersonExperimental(message)
            for i in range(len(initiator.conference)):
                if initiator.conference[i] == message['peer_id'] - 2000000000:
                    if (initiator.rang[i] >= 1) and (initiator.rang[i] > experimental.rang[i]):
                        self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                            member_id=int(message['text'][5:].split("|")[0].replace("[id", "")))
                        self.send_msg(message['peer_id'], f"{initiator.nick[i]} исключил {experimental.nick[i]}")
                        experimental.remConf(message['peer_id'] - 2000000000)
                        break
                    else:
                        self.send_msg(message['peer_id'], "Недостаточно прав")
                        break

        if "/hi" in message['text']:
            for i in range(len(initiator.conference)):
                if initiator.conference[i] == message['peer_id'] - 2000000000:
                    if initiator.rang[i] >= 2:
                        conf.setHi(message['text'][3:])
                        self.send_msg(message['peer_id'], f"Приветственное сообщение установлено!")
                        break
                    else:
                        self.send_msg(message['peer_id'], "Недостаточно прав")
                        break

        if "/rang" in message['text']:
            experimental = PersonExperimental(message)
            for i in range(len(initiator.conference)):
                if initiator.conference[i] == message['peer_id'] - 2000000000:
                    if (initiator.rang[i] >= 2) and (initiator.rang[i] > experimental.rang[i]):
                        experimental.setRang(message['text'], conf.id)
                        self.send_msg(message['peer_id'], f"Права модератора обновлены")
                        break
                    else:
                        self.send_msg(message['peer_id'], "Недостаточно прав")
                        break

        if "/snick" in message['text']:
            experimental = PersonExperimental(message)
            for i in range(len(initiator.conference)):
                if initiator.conference[i] == message['peer_id'] - 2000000000:
                    if (initiator.rang[i] >= 1) and (initiator.rang[i] >= experimental.rang[i]):
                        experimental.setNick(message['text'], conf.id)
                        self.send_msg(message['peer_id'], f"Никнейм пользователя изменён на {experimental.nick}")
                        break
                    else:
                        self.send_msg(message['peer_id'], "Недостаточно прав")
                        break

        if "/warn" in message['text']:
            experimental = PersonExperimental(message)
            for i in range(len(initiator.conference)):
                if initiator.conference[i] == message['peer_id'] - 2000000000:
                    if (initiator.rang[i] >= 3) and (initiator.rang[i] > experimental.rang[i]):
                        experimental.addWarn(message['peer_id'] - 2000000000)
                        self.send_msg(message['peer_id'], f"{initiator.nick[i]} выдал предупреждение {experimental.nick[i]} [{experimental.warn[i]}/3]")
                        break
                    else:
                        self.send_msg(message['peer_id'], "Недостаточно прав")
                        break
            if experimental.warn[i] >= 3:
                self.send_msg(message['peer_id'], f"{experimental.nick[i]} получил 3/3 предупреждений")
                experimental.remConf(message['peer_id'] - 2000000000)
                self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                    member_id=int(experimental.id))

        if "/unwarn" in message['text']:
            experimental = PersonExperimental(message)
            for i in range(len(initiator.conference)):
                if initiator.conference[i] == message['peer_id'] - 2000000000:
                    if (initiator.rang[i] >= 3) and (initiator.rang[i] > experimental.rang[i]):
                        if experimental.warn[i] == 0:
                            self.send_msg(message['peer_id'], f"У {experimental.nick[i]} нет активных предупреждений")
                            break
                        else:
                            experimental.delWarn(message['peer_id'] - 2000000000)
                            self.send_msg(message['peer_id'], f"{initiator.nick[i]} снял предупреждение у {experimental.nick[i]} [{experimental.warn[i]}/3]")
                            break
                    else:
                        self.send_msg(message['peer_id'], "Недостаточно прав")
                        break

        if "/cmd" in message['text']:
            for i in range(len(initiator.conference)):
                if initiator.conference[i] == message['peer_id'] - 2000000000:
                    if (initiator.rang[i] >=1 ) and (initiator.rang[i] > experimental.rang[i]):
                             self.send_msg(message['peer_id'],f" {initiator.nick[i]} Cписок доступных команд")






    def action(self, message):
        conf = Conference(message['peer_id'] - 2000000000)  # получение информации о конфе в которой написали команду
        # приветственное сообщение при инвайте нового пользователя
        experimental = PersonExperimental(message,
                                          name=self.vk_api.users.get(user_ids=message["action"]["member_id"],
                                                                     fields="screen_name"))
        if message['action']['type'] == 'chat_invite_user':
            experimental.addConf(message['peer_id'] - 2000000000,
                                 self.vk_api.users.get(user_ids=message['action']['member_id'], fields="screen_name"))
            self.send_msg(message['peer_id'], conf.hi)
        # кик игрока, который вышел
        if message['action']['type'] == 'chat_kick_user':
            experimental.remConf(message['peer_id'] - 2000000000)
            if message['from_id'] == message['action']['member_id']:
                self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                    member_id=int(message['from_id']))
