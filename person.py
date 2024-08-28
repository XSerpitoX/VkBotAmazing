import psycopg2
from config import host, user, password, db_name


class PersonInitiator:
    def __init__(self, info, name):
        if 'action' in info:
            self.id = info['action']['member_id']
        else:
            self.id = info['from_id']
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        nname = name[0]['first_name'] + " " + name[0]['last_name']
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            print(value)
            if value is None:
                cursor.execute(
                    f"""INSERT INTO "Person" VALUES(
                            '{self.id}',
                            ARRAY[]::text[],
                            ARRAY[]::integer[],
                            ARRAY[]::integer[],
                            ARRAY[]::integer[],
                            '{nname}');""")
                connection.commit()
                cursor.execute(
                    f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
                value = cursor.fetchone()
            self.nick = value[1]
            self.rang = value[2]
            self.conference = value[3]
            self.warn = value[4]
            self.name = value[5]
            if len(self.conference) >= 2:
                if self.conference[0] == self.conference[1]:
                    self.nick.pop(1)
                    self.rang.pop(1)
                    self.conference.pop(1)
                    self.warn.pop(1)
                    cursor.execute(
                        f"""UPDATE "Person" SET nick = ARRAY{self.nick}::text[],
                                                                rang = ARRAY{self.rang}::integer[],
                                                                conference = ARRAY{self.conference}::integer[], 
                                                                warn = ARRAY{self.warn}::integer[],
                                                                name = '{nname}'
                                                        WHERE "ID" = {self.id};""")
                    connection.commit()
            connection.close()
            cursor.close()

    def addConf(self, id_conf, nick='["Ник не указан"]'):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            print(nick)
            name = f"{nick[0]['first_name']} {nick[0]['last_name']}"
            print(value)
            value[1].append(name)
            value[2].append(0)
            value[3].append(id_conf)
            value[4].append(0)
            print(value)
            cursor.execute(
                f"""UPDATE "Person" SET nick = ARRAY{value[1]}::text[],
                                            rang = ARRAY{value[2]}::integer[],
                                            conference = ARRAY{value[3]}::integer[], 
                                            warn = ARRAY{value[4]}::integer[],
                                            name = '{name}'
                                    WHERE "ID" = {self.id};""")
            connection.commit()
            connection.close()
            cursor.close()


class PersonExperimental:
    def __init__(self, info, name):
        if 'action' in info:
            if info['action']['type'] == 'chat_invite_user':
                self.id = info['action']['member_id']
            else:
                self.id = info['from_id']
        else:
            self.id = info['text'].split(" ")[1].split('|')[0].replace('[id', '')
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        nname = name[0]['first_name'] + " " + name[0]['last_name']
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            if value is None:
                cursor.execute(
                    f"""INSERT INTO "Person" VALUES(
                            '{self.id}',
                            ARRAY[]::text[],
                            ARRAY[]::integer[],
                            ARRAY[]::integer[],
                            ARRAY[]::integer[],
                            '{nname}');""")
                connection.commit()
                cursor.execute(
                    f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
                value = cursor.fetchone()
            self.nick = value[1]
            self.rang = value[2]
            self.conference = value[3]
            self.warn = value[4]
            self.name = value[5]
            if len(self.conference) >= 2:
                if self.conference[0] == self.conference[1]:
                    self.nick.pop(1)
                    self.rang.pop(1)
                    self.conference.pop(1)
                    self.warn.pop(1)
                    cursor.execute(
                        f"""UPDATE "Person" SET nick = ARRAY{self.nick}::text[],
                                                                rang = ARRAY{self.rang}::integer[],
                                                                conference = ARRAY{self.conference}::integer[], 
                                                                warn = ARRAY{self.warn}::integer[],
                                                                name = '{nname}'
                                                        WHERE "ID" = {self.id};""")
                    connection.commit()
            connection.close()
            cursor.close()

    def setRang(self, message, id_conf):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            a = value[2]
            b = value[3]
            print(a)
            print(b)
            print(b.index(id_conf) + 1)
            print(message.split(" ")[-1])
            cursor.execute(
                f"""UPDATE "Person" SET rang[{b.index(id_conf) + 1}] = '{message.split(" ")[-1]}'
                        WHERE "ID" = {self.id};""")
            connection.commit()
            connection.close()
            cursor.close()

    def setNick(self, message, id_conf):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            a = value[2]
            b = value[3]
            print(a)
            print(b)
            cursor.execute(
                f"""UPDATE "Person" SET nick[{b.index(id_conf) + 1}] = '{" ".join(message.split(" ")[2:])}'
                                WHERE "ID" = {self.id};""")
            self.nick = " ".join(message.split(" ")[2:])
            connection.commit()
            connection.close()
            cursor.close()

    def addConf(self, id_conf, nick='["Ник не указан"]'):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()

            name = f"{nick[0]['first_name']} {nick[0]['last_name']}"
            print(value)
            value[1].append(name)
            value[2].append(0)
            value[3].append(id_conf)
            value[4].append(0)
            print(value)
            cursor.execute(
                f"""UPDATE "Person" SET nick = ARRAY{value[1]}::text[],
                                        rang = ARRAY{value[2]}::integer[],
                                        conference = ARRAY{value[3]}::integer[], 
                                        warn = ARRAY{value[4]}::integer[],
                                        name = '{name}'
                                WHERE "ID" = {self.id};""")
            connection.commit()
            connection.close()
            cursor.close()

    def remConf(self, id_conf):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            nick = value[1]
            rang = value[2]
            conf = value[3]
            warn = value[4]
            f = conf.index(id_conf)
            nick.pop(f)
            rang.pop(f)
            conf.remove(id_conf)
            warn.pop(f)
            print(f)
            cursor.execute(
                f"""UPDATE "Person" SET nick = ARRAY{nick}::text[],
                                        rang = ARRAY{rang}::integer[],
                                        conference = ARRAY{conf}::integer[], 
                                        warn = ARRAY{warn}::integer[]
                                WHERE "ID" = {self.id};""")
            connection.commit()
            connection.close()
            cursor.close()

    def addWarn(self, id_conf):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            a = value[4]
            b = value[3]
            print(a)
            print(b)
            cursor.execute(
                f"""UPDATE "Person" SET warn[{b.index(id_conf) + 1}] = '{a[b.index(id_conf)] + 1}'
                                        WHERE "ID" = {self.id};""")
            self.warn[b.index(id_conf)] += 1
            connection.commit()
            connection.close()
            cursor.close()

    def delWarn(self, id_conf):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            a = value[4]
            b = value[3]
            print(a)
            print(b)
            cursor.execute(
                f"""UPDATE "Person" SET warn[{b.index(id_conf) + 1}] = '{a[b.index(id_conf)] - 1}'
                                        WHERE "ID" = {self.id};""")
            self.warn[b.index(id_conf)] -= 1
            connection.commit()
            connection.close()
            cursor.close()


def nlist(id_conf):
    ans = "Имя пользователя - Ник пользователя \n"
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT * FROM public."Person";""")
        values = cursor.fetchall()
        connection.close()
        cursor.close()
        for value in values:
            if id_conf in value[3]:
                ans += f"https://vk.com/id{value[0]} - {value[1][value[3].index(id_conf)]} \n"

        return ans


def getAllID():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT "ID" FROM public."Person";""")
        values = cursor.fetchall()
        connection.close()
        cursor.close()
        return values


def addName(id, name):
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    nname = name[0]['first_name'] + " " + name[0]['last_name']
    if "'" in nname:
        nname = str(nname.replace("'", ""))
    com = f"""UPDATE public."Person" SET name = '{nname}' WHERE "ID" = {int(str(id)[1:-2])};"""
    print(com)
    with connection.cursor() as cursor:
        cursor.execute(com)
        connection.commit()
        connection.close()
        cursor.close()


class PersonParse:
    def __init__(self, conf_id, data):
        self.id = data[0]['id']
        self.name = data[0]['first_name'] + " " + data[0]['last_name']
        if "'" in self.name:
            self.name = str(self.name.replace("'", ""))
        print(self.id, self.name)
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            if value is None:
                cursor.execute(
                    f"""INSERT INTO "Person" VALUES(
                                        '{self.id}',
                                        ARRAY[]::text[],
                                        ARRAY[]::integer[],
                                        ARRAY[]::integer[],
                                        ARRAY[]::integer[],
                                        '{self.name}');""")
                connection.commit()
                cursor.execute(
                    f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
                value = cursor.fetchone()
                print(value)
                value[1].append(self.name)
                value[2].append(0)
                value[3].append(conf_id)
                value[4].append(0)
                print(value)
                cursor.execute(
                    f"""UPDATE "Person" SET nick = ARRAY{value[1]}::text[],
                                                        rang = ARRAY{value[2]}::integer[],
                                                        conference = ARRAY{value[3]}::integer[], 
                                                        warn = ARRAY{value[4]}::integer[],
                                                        name = '{self.name}'::text
                                                WHERE "ID" = {self.id};""")
                connection.commit()
                cursor.execute(
                    f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
                value = cursor.fetchone()
            a = value[3]
            print(value[3])
            if not (conf_id in a):
                value[1].append(self.name)
                value[2].append(0)
                value[3].append(conf_id)
                value[4].append(0)
                cursor.execute(
                    f"""UPDATE "Person" SET nick = ARRAY{value[1]}::text[],
                                                            rang = ARRAY{value[2]}::integer[],
                                                            conference = ARRAY{value[3]}::integer[],
                                                            warn = ARRAY{value[4]}::integer[],
                                                            name = '{self.name}'::text
                                                    WHERE "ID" = {self.id};""")
                connection.commit()
            connection.close()
            cursor.close()
