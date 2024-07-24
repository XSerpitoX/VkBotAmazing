import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from vk_api import VkUpload
import random
from pprint import pprint
import urllib.request
import os
from PIL import Image
import person

from conference import Conference, ConferenceCluster
from person import PersonInitiator, PersonExperimental, PersonParse


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
        self.vk_upload = VkUpload(self.vk_api)

    def send_msg(self, send_id, message):
        self.vk_api.messages.send(peer_id=send_id, message=message, random_id=random.randint(0, 6000))

    def send_photo(self, send_id, message, photo):
        self.vk_api.messages.send(peer_id=send_id, message=message, attachment=photo, random_id=random.randint(0, 6000))

    def test(self):
        # Посылаем сообщение пользователю с указанным ID
        self.send_msg(384407860, "Привет-привет!")
        pprint(self.vk_api.users.get(user_ids="384407860", fields="screen_name"))

    def start(self):
        # conf = ConferenceCluster() # 129, 125
        # print(conf.value)
        # for i in range(len(conf.value)):
        #     conf_id = conf.value[i][0]
        #     print(conf_id)
        #     members = self.vk_api.messages.getConversationMembers(peer_id=2000000000 + conf_id)['items']
        #     for j in range(len(members)):
        #         member = members[j]['member_id']
        #         if member >= 0:
        #             PersonParse(conf_id, self.vk_api.users.get(user_ids=member))
        print("БОТ ЗАПУЩЕН")
        for event in self.long_poll.listen():  # Слушаем сервер
            if event.type == VkBotEventType.MESSAGE_NEW:
                pprint(event.message)
                if "/" in event.message['text']:
                    if event.message['text'][0] == "/":
                        self.command(event.message)
                if 'action' in event.message:
                    self.action(event.message)
                if "#" in event.message['text']:
                    self.shipping(event.message)

    def command(self, message):
        conf = Conference(message['peer_id'] - 2000000000)  # получение информации о конфе в которой написали команду
        if conf.hi is None:
            self.send_msg(message['peer_id'],
                          f"Бот не авторизован. Дальнейшая работа будет доступна после авторизации. \n \n Обратитесь к разработчикам")
        else:
            initiator = PersonInitiator(message,
                                        self.vk_api.users.get(user_ids=message['from_id'], fields="screen_name"))
            pprint(f"В конфу {conf.name} Пользователь {initiator.name} написал {message['text']}")
            if "/test" in message['text']:
                self.send_msg(message['peer_id'], f"Бот работает!")

            if "/kick" in message['text']:
                experimental = PersonExperimental(message, self.vk_api.users.get(
                    user_ids=int(message['text'][5:].split("|")[0].replace("[id", "")),
                    fields="screen_name"))
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        for j in range(len(experimental.conference)):
                            if (initiator.rang[i] >= 2) and (initiator.rang[i] > experimental.rang[j]):
                                self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                                    member_id=int(
                                                                        message['text'][5:].split("|")[0].replace("[id",
                                                                                                                  "")))
                                self.send_msg(message['peer_id'],
                                              f"@id{initiator.id}({initiator.nick[i]}) исключил @id{experimental.id}({experimental.nick[j]})")
                                experimental.remConf(message['peer_id'] - 2000000000)
                                break
                            else:
                                self.send_msg(message['peer_id'], "Недостаточно прав")
                                break

            if "/allkick" in message['text']:
                experimental = PersonExperimental(message, self.vk_api.users.get(
                    user_ids=int(message['text'][8:].split("|")[0].replace("[id", "").strip()),
                    fields="screen_name"))
                for i in range(len(initiator.conference)):
                    if initiator.rang[i] >= 5:
                        for j in range(len(experimental.conference)):
                            if initiator.conference[i] == experimental.conference[j]:
                                if initiator.rang[i] > experimental.rang[j]:
                                    experimental.remConf(experimental.conference[j])
                                    self.vk_api.messages.removeChatUser(chat_id=experimental.conference[j],
                                                                        member_id=experimental.id)
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
                experimental = PersonExperimental(message, self.vk_api.users.get(
                    user_ids=int(message['text'][5:].split("|")[0].replace("[id", "")),
                    fields="screen_name"))
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        for j in range(len(experimental.conference)):
                            if (initiator.rang[i] >= 2) and (initiator.rang[i] > experimental.rang[j]) and (
                                    initiator.rang[i] > int(message['text'].split(' ')[-1])):
                                experimental.setRang(message['text'], conf.id)
                                self.send_msg(message['peer_id'],
                                              f"Права модератора обновлены. Уровень доступа: {message['text'].split(' ')[-1]} \n \n Для просмотра функционала — /cmd")
                                break
                            else:
                                self.send_msg(message['peer_id'], "Недостаточно прав")
                                break

            if "/allrang" in message['text']:
                going = False
                experimental = PersonExperimental(message, self.vk_api.users.get(
                    user_ids=int(message['text'][8:].split("|")[0].replace("[id", "").strip()),
                    fields="screen_name"))
                for i in range(len(initiator.conference)):
                    if initiator.rang[i] >= 5:
                        for j in range(len(experimental.conference)):
                            if initiator.conference[i] == experimental.conference[j]:
                                if initiator.rang[i] >= experimental.rang[j]:
                                    experimental.setRang(message['text'], experimental.conference[j])
                                    going = True
                    else:
                        self.send_msg(message['peer_id'], "Недостаточно прав")
                        break
                if going:
                    self.send_msg(2000000157,
                                  f"@id{initiator.id}({initiator.name}) изменил права модератора во всех беседах пользователю @id{experimental.id}({experimental.name}) \n \n Уровень доступа: {message['text'].split(' ')[-1]}")
                    self.send_msg(experimental.id,
                                  f"Вам выданы права модератора во всех беседах, в которых Вы состоите \n \n Уровень доступа: {message['text'].split(' ')[-1]}")

            if "/snick" in message['text']:
                experimental = PersonExperimental(message, self.vk_api.users.get(
                    user_ids=int(message['text'][6:].split("|")[0].replace("[id", "")),
                    fields="screen_name"))
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        for j in range(len(experimental.conference)):
                            if (initiator.rang[i] >= 1) and (initiator.rang[i] >= experimental.rang[j]):
                                experimental.setNick(message['text'], conf.id)
                                self.send_msg(message['peer_id'],
                                              f"Никнейм пользователя изменён на @id{experimental.id}({experimental.nick})")
                                break
                            else:
                                self.send_msg(message['peer_id'], "Недостаточно прав")
                                break

            if "/allnick" in message['text']:
                going = False
                experimental = PersonExperimental(message, self.vk_api.users.get(
                    user_ids=int(message['text'][8:].split("|")[0].replace("[id", "").strip()),
                    fields="screen_name"))
                for i in range(len(initiator.conference)):
                    if initiator.rang[i] >= 4:
                        for j in range(len(experimental.conference)):
                            if initiator.conference[i] == experimental.conference[j]:
                                if initiator.rang[i] >= experimental.rang[j]:
                                    experimental.setNick(message['text'], experimental.conference[j])
                                    going = True

                    else:
                        self.send_msg(message['peer_id'], "Недостаточно прав")
                        break

                if going:
                    self.send_msg(message['peer_id'],
                                  f"Вы установили пользователю @id{experimental.id}({experimental.name}) имя во всех беседах — «{' '.join(message['text'].split(' ')[2:])}»")
                    self.send_msg(experimental.id,
                                  f"@id{initiator.id}({initiator.nick[i]}) установил Вам во всех беседах имя пользователя — «{' '.join(message['text'].split(' ')[2:])}»")

            if "/warn" in message['text']:
                experimental = PersonExperimental(message, self.vk_api.users.get(
                    user_ids=int(message['text'][5:].split("|")[0].replace("[id", "")),
                    fields="screen_name"))
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        for j in range(len(experimental.conference)):
                            if initiator.conference[i] == experimental.conference[j]:
                                if (initiator.rang[i] >= 3) and (initiator.rang[i] > experimental.rang[j]):
                                    experimental.addWarn(message['peer_id'] - 2000000000)
                                    self.send_msg(message['peer_id'],
                                                  f"@id{initiator.id}({initiator.nick[i]}) выдал предупреждение @id{experimental.id}({experimental.nick[j]}) [{experimental.warn[j]}/3]")
                                    break
                                else:
                                    self.send_msg(message['peer_id'], "Недостаточно прав")
                                    break
                        if experimental.warn[j] >= 3:
                            self.send_msg(message['peer_id'],
                                          f"@id{experimental.id}({experimental.nick[j]}) получил 3/3 предупреждений")
                            self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                                member_id=int(experimental.id))
                            experimental.remConf(message['peer_id'] - 2000000000)

            if "/unwarn" in message['text']:
                experimental = PersonExperimental(message, self.vk_api.users.get(
                    user_ids=int(message['text'][7:].split("|")[0].replace("[id", "")),
                    fields="screen_name"))
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        for j in range(len(experimental.conference)):
                            if (initiator.rang[i] >= 3) and (initiator.rang[i] > experimental.rang[j]):
                                if (experimental.warn[j]) == 0 and (
                                        experimental.conference[j] == message['peer_id'] - 2000000000):
                                    self.send_msg(message['peer_id'],
                                                  f"У @id{experimental.id}({experimental.nick[j]}) нет активных предупреждений")
                                    break
                                else:
                                    experimental.delWarn(message['peer_id'] - 2000000000)
                                    self.send_msg(message['peer_id'],
                                                  f"@id{initiator.id}({initiator.nick[i]}) снял предупреждение у @id{experimental.id}({experimental.nick[j]}) [{experimental.warn[j]}/3]")
                                    break
                            else:
                                self.send_msg(message['peer_id'], "Недостаточно прав")
                                break

            if "/cmd" in message['text']:
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        ans = f"Ваш уровень доступа: {initiator.rang[i]} \n \n Список доступных команд: \n"
                        if initiator.rang[i] >= 0:
                            ans += "/cmd — информация о доступном функционале \n" \
                                   "/nlist — посмотреть список установленных имен \n" \
                                   "/lvl — посмотреть уровни доступа модераторов \n" \
                                   "/pw — посмотреть пароль от закрытой темы на форуме"
                        if initiator.rang[i] >= 1:
                            ans += "/kick — исключить пользователя из беседы \n" \
                                   "/snick — установить пользователю индивидуальный никнейм \n"
                        if initiator.rang[i] >= 2:
                            ans += "/hi — установить приветствие в беседе \n" \
                                   "/rang — выдать права модератора пользователю \n"
                        if initiator.rang[i] >= 3:
                            ans += "/warn — выдать предупреждение пользователю за нарушение правил поведения в беседе \n" \
                                   "/unwarn — снять предупреждение \n"
                        if initiator.rang[i] >= 4:
                            ans += "/allnick — установить индивидуальный никнейм пользователю во всех беседах \n"
                        if initiator.rang[i] >= 5:
                            ans += "/allkick — исключить пользователя из всех бесед, в которых состоит пользователь \n"
                        if initiator.rang[i] >= 6:
                            ans += "/msg — отправить массовую рассылку сообщения \n" \
                                   "/allrang — выдать уровень доступа к модерации во всех беседах \n"
                        self.send_msg(message['peer_id'], ans)
            if "/nlist" in message['text']:
                self.send_msg(message['peer_id'], person.nlist(message['peer_id'] - 2000000000))

            if "/help" in message['text']:
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        self.send_msg(message['peer_id'], f"Важная информация: ")

            if "/parse" in message['text']:
                id_conf = int(message['text'].split()[1])
                members = self.vk_api.messages.getConversationMembers(peer_id=2000000000 + id_conf)['items']
                for i in range(len(members)):
                    member = members[i]['member_id']
                    if member >= 0:
                        PersonParse(id_conf, self.vk_api.users.get(user_ids=member))

            if "/lvl" in message['text']:
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        self.send_msg(message['peer_id'], f"Уровни доступа к модерированию беседы: \n"
                                                          f"\n 0 — обычный пользователь "
                                                          f"\n 1 — начальники подразделений, заместители лидера "
                                                          f"\n 2 — лидер "
                                                          f"\n 3 — следящий администратор "
                                                          f"\n 4 — заместитель куратора "
                                                          f"\n 5 — куратор "
                                                          f"\n 6 — заместитель главного администратора "
                                                          f"\n 7 — главный администратор")

            if "/msg" in message['text']:
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if initiator.rang[i] >= 6:
                            print(message['text'].split(' ')[1])
                            conf = ConferenceCluster(int(message['text'].split(' ')[1]))
                            for j in range(len(conf.value)):
                                conf_id = conf.value[j][0]
                                self.send_msg(2000000000 + conf_id, ' '.join(message['text'].split(' ')[2:]))
                        else:
                            self.send_msg(message['peer_id'], "Недостаточно прав")
                            break

            if "/password" in message['text']:
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if initiator.rang[i] >= 7:
                            category_pass = int(message['text'].split(' ')[1])
                            password = str(message['text'].split(' ')[2])
                            conf.setPassword(category_pass, password)
                            self.send_msg(2000000157, f"Пароль для категории {category_pass} был изменён на {password}")
                        else:
                            self.send_msg(message['peer_id'], "Недостаточно прав")
                            break

            if "/pw" in message['text']:
                if not (conf.password is None):
                    self.send_msg(message['peer_id'], f"Текущий пароль — {conf.password} \n \n"
                                                      f"⛔ Администрация сервера напоминает об ответственности в виде блокировки аккаунта на 30 дней за разглашение пароля и информации из приватного форумного раздела организации третьим лицам")
                else:
                    self.send_msg(message['peer_id'], f"Пароль отсутствует")

            if "/logo" in message['text']:
                for i in range(len(message['attachments'])):
                    urllib.request.urlretrieve(message['attachments'][i]['photo']['orig_photo']['url'],
                                               "photo_from_logo.png")
                    filename = "photo_from_logo.png"
                    logo = "LOGO_AZURE.png"
                    with Image.open(filename) as img:
                        img.load()
                    with Image.open(logo) as img_logo:
                        img_logo.load()

                    img_logo = img_logo.reduce(5)
                    img.paste(img_logo,
                              ((img.size[0] // 2 - img_logo.size[0] // 2), (img.size[1] - img_logo.size[1] - 40)),
                              img_logo)
                    img.save("photo_from_logo.png")
                    upload_image = \
                        self.vk_upload.photo_messages(photos="photo_from_logo.png", peer_id=message['peer_id'])[0]
                    self.send_photo(message['peer_id'], "",
                                    'photo{}_{}'.format(upload_image['owner_id'], upload_image['id']))
                    os.remove("photo_from_logo.png")

            if "/remove" in message['text']:
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if initiator.rang[i] >= 5:
                            experimental = PersonExperimental(message, self.vk_api.users.get(
                                user_ids=int(message['text'][7:].split("|")[0].replace("[id", "")),
                                fields="screen_name"))
                            experimental.remConf(message['peer_id'] - 2000000000)
                            self.send_msg(message['peer_id'], f"Пользователь удалён из базы")
                        else:
                            self.send_msg(message['peer_id'], "Недостаточно прав")
                            break

            if "/devnick" in message['text']:
                for i in range(len(initiator.conference)):
                    if initiator.conference[i] == message['peer_id'] - 2000000000:
                        if initiator.rang[i] >= 10:
                            id = person.getAllID()
                            print(id)
                            for j in range(len(id)):
                                person.addName(id[j], self.vk_api.users.get(user_ids=id[j], fields="screen_name"))

    def action(self, message):
        conf = Conference(message['peer_id'] - 2000000000)  # получение информации о конфе в которой написали команду
        print(message)
        if conf.hi is None:
            self.send_msg(message['peer_id'],
                          f"Бот не авторизован. Дальнейшая работа будет доступна после авторизации. \n \n Обратитесь к разработчикам")
        else:
            print()
            experimental = PersonExperimental(message,
                                              name=self.vk_api.users.get(user_ids=message["action"]["member_id"],
                                                                         fields="screen_name"))
            # приветственное сообщение при инвайте нового пользователя
            if message['action']['type'] == 'chat_invite_user':
                experimental.addConf(message['peer_id'] - 2000000000,
                                     self.vk_api.users.get(user_ids=message['action']['member_id'],
                                                           fields="screen_name"))
                self.send_msg(message['peer_id'], conf.hi)
            # кик игрока, который вышел
            if message['action']['type'] == 'chat_kick_user':
                experimental.remConf(message['peer_id'] - 2000000000)
                if message['from_id'] == message['action']['member_id']:
                    self.vk_api.messages.removeChatUser(chat_id=message['peer_id'] - 2000000000,
                                                        member_id=int(message['from_id']))

    def shipping(self, message):
        conf = Conference(message['peer_id'] - 2000000000)
        if conf.hi is None:
            self.send_msg(message['peer_id'],
                          f"Бот не авторизован. Дальнейшая работа будет доступна после авторизации. \n \n Обратитесь к разработчикам")
        else:
            initiator = PersonInitiator(message,
                                        self.vk_api.users.get(user_ids=message['from_id'], fields="screen_name"))
            if "#призыв" in message['text'] or "#собес" in message['text']:
                if "Правительство" in conf.name: sled_id = 169
                if "ТРК" in conf.name:
                    sled_id = 166
                elif "ВЧ" in conf.name:
                    sled_id = 167
                elif "ЕСС" in conf.name:
                    sled_id = 163
                elif "УФСИН" in conf.name:
                    sled_id = 165
                elif "ГАИ" in conf.name or "УМВД" in conf.name:
                    sled_id = 161
                else:
                    sled_id = None
                if sled_id is None:
                    pass
                else:
                    self.send_msg(2000000000 + sled_id, f"{initiator.nick[initiator.conference.index(conf.id)]} провёл набор в организацию \n \n"
                                                        f"Полное сообщение: {message['text']}")
                print(f"{initiator.nick[initiator.conference.index(conf.id)]} провёл набор в организацию \n \n"
                                                        f"Полное сообщение: {message['text']}")
