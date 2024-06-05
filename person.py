import psycopg2
from config import host, user, password, db_name


class PersonInitiator:
    def __init__(self, info, name='[Ник не указан]'):
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
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
            value = cursor.fetchone()
            print(value)
            if value is None:
                nick = name
                rang = '{0}'
                conf = info['peer_id'] - 2000000000
                warn = '{0}'
                cursor.execute(
                    f"""INSERT INTO "Person" VALUES(
                    '{self.id}',
                    ARRAY[{nick}]::text[],
                    '{rang}',
                    '{{{conf}}}',
                    '{warn}');""")
                connection.commit()
                cursor.execute(
                    f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
                value = cursor.fetchone()
            self.nick = value[1]
            self.rang = value[2]
            self.conference = value[3]
            self.warn = value[4]
            connection.close()
            cursor.close()


class PersonExperimental:
    def __init__(self, info, name='["Ник не указан"]'):
        if 'action' in info:
            self.id = info['action']['member_id']
        else:
            self.id = info['text'].split(" ")[1].split('|')[0].replace('[id', '')
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
                rang = '{0}'
                conf = info['peer_id'] - 2000000000
                warn = '{0}'
                cursor.execute(
                    f"""INSERT INTO "Person" VALUES(
                            '{self.id}',
                            ARRAY[]::text[],
                            ARRAY[]::integer[],
                            ARRAY[]::integer[],
                            ARRAY[]::integer[]);""")
                connection.commit()
                cursor.execute(
                    f"""SELECT * FROM "Person" WHERE "ID" = {self.id};""")
                value = cursor.fetchone()
            self.nick = value[1]
            self.rang = value[2]
            self.conference = value[3]
            self.warn = value[4]
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
            print(nick)
            if nick != '["Ник не указан"]':
                name = f"{nick[0]['first_name']} {nick[0]['last_name']}"
            else:
                name = nick
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
                                        warn = ARRAY{value[4]}::integer[]
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
            c = value[1]
            d = value[4]
            a = value[2]
            b = value[3]
            f = b.index(id_conf)
            a.pop(f)
            c.pop(f)
            d.pop(f)
            b.remove(id_conf)
            print(b)
            cursor.execute(
                f"""UPDATE "Person" SET nick = ARRAY{c}::text[],
                                        rang = ARRAY{a}::integer[],
                                        conference = ARRAY{b}::integer[], 
                                        warn = ARRAY{d}::integer[]
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
                f"""UPDATE "Person" SET warn[{b.index(id_conf) + 1}] = '{a[b.index(id_conf)]+1}'
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
                f"""UPDATE "Person" SET warn[{b.index(id_conf) + 1}] = '{a[b.index(id_conf)]-1}'
                                        WHERE "ID" = {self.id};""")
            self.warn[b.index(id_conf)] -= 1
            connection.commit()
            connection.close()
            cursor.close()
