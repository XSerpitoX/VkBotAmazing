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
                if "/" in event.message['text']:
                    self.command(event.message)
                if 'action' in event.message:
                    self.action(event.message)

    def command(self, message):
        conf = Conference(message['peer_id'] - 2000000000)  # получение информации о конфе в которой написали команду
        print(message)
        if conf.hi is None:
            self.send_msg(message['peer_id'], f"Бот не авторизован. Дальнейшая работа будет доступна после авторизации. \n \n Обратитесь к разработчикам")
        else:
            initiator = PersonInitiator(message)
            if "/test" in message['text']:
                self.send_msg(message['peer_id'], f"Бот работает!")

            if "/kick" in message['text']:
                experimental = PersonExperimental(message)
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if (initiator.rang[i] >= 1) and (initiator.rang[i] > experimental.rang[i]):
                            self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                                member_id=int(
                                                                    message['text'][5:].split("|")[0].replace("[id", "")))
                            self.send_msg(message['peer_id'], f"@id{initiator.id}({initiator.nick[i]}) исключил @id{experimental.id}({experimental.nick[i]})")
                            experimental.remConf(message['peer_id'] - 2000000000)
                            break
                        else:
                            self.send_msg(message['peer_id'], "Недостаточно прав")
                            break

            if "/allkick" in message['text']:
                experimental = PersonExperimental(message)
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if (initiator.rang[i] >= 3) and (initiator.rang[i] > experimental.rang[i]):
                            l = experimental.conference
                            for j in range(len(l)):
                                if initiator.rang[i] > experimental.rang[j]:
                                    print(experimental.conference[j])
                                    self.vk_api.messages.removeChatUser(chat_id=l[j],
                                                                        member_id=int(
                                                                    message['text'][8:].split("|")[0].replace("[id", "")))
                                    experimental.remConf(l[j])
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
                            self.send_msg(message['peer_id'], f"Никнейм пользователя изменён на @id{experimental.id}({experimental.nick})")
                            break
                        else:
                            self.send_msg(message['peer_id'], "Недостаточно прав")
                            break

            if "/allnick" in message['text']:
                experimental = PersonExperimental(message)
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if (initiator.rang[i] >= 3) and (initiator.rang[i] > experimental.rang[i]):
                            l = experimental.conference
                            for j in range(len(l)):
                                if initiator.rang[i] > experimental.rang[j]:
                                    print(experimental.conference[j])
                                    experimental.setNick(message['text'], l[j])
                        else:
                            self.send_msg(message['peer_id'], "Недостаточно прав")
                            break

            if "/warn" in message['text']:
                experimental = PersonExperimental(message)
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if (initiator.rang[i] >= 3) and (initiator.rang[i] > experimental.rang[i]):
                            experimental.addWarn(message['peer_id'] - 2000000000)
                            self.send_msg(message['peer_id'],
                                          f"@id{initiator.id}({initiator.nick[i]}) выдал предупреждение @id{experimental.id}({experimental.nick[i]}) [{experimental.warn[i]}/3]")
                            break
                        else:
                            self.send_msg(message['peer_id'], "Недостаточно прав")
                            break
                if experimental.warn[i] >= 3:
                    self.send_msg(message['peer_id'], f"@id{experimental.id}({experimental.nick[i]}) получил 3/3 предупреждений")
                    experimental.remConf(message['peer_id'] - 2000000000)
                    self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                        member_id=int(experimental.id))

            if "/unwarn" in message['text']:
                experimental = PersonExperimental(message)
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if (initiator.rang[i] >= 3) and (initiator.rang[i] > experimental.rang[i]):
                            if experimental.warn[i] == 0:
                                self.send_msg(message['peer_id'], f"У @id{experimental.id}({experimental.nick[i]}) нет активных предупреждений")
                                break
                            else:
                                experimental.delWarn(message['peer_id'] - 2000000000)
                                self.send_msg(message['peer_id'],
                                              f"@id{initiator.id}({initiator.nick[i]}) снял предупреждение у @id{experimental.id}({experimental.nick[i]}) [{experimental.warn[i]}/3]")
                                break
                        else:
                            self.send_msg(message['peer_id'], "Недостаточно прав")
                            break

    def action(self, message):
        conf = Conference(message['peer_id'] - 2000000000)  # получение информации о конфе в которой написали команду
        print(message)
        if conf.hi is None:
            self.send_msg(message['peer_id'], f"Бот не авторизован. Дальнейшая работа будет доступна после авторизации. \n \n Обратитесь к разработчикам")
        else:
            experimental = PersonExperimental(message,
                                              name=self.vk_api.users.get(user_ids=message["action"]["member_id"],
                                                                         fields="screen_name"))
            # приветственное сообщение при инвайте нового пользователя
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
