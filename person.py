import psycopg2
from config import host, user, password, db_name


class PersonInitiator:
    def __init__(self, info):
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
            if value == None:
                nick = '{"Ник не указан"}'
                rang = '{0}'
                conf = info['peer_id'] - 2000000000
                warn = '{0}'
                cursor.execute(
                    f"""INSERT INTO "Person" VALUES(
                    '{self.id}',
                    '{nick}',
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
    def __init__(self, info):
        self.id = info['text'].split(" ")[1].split('|')[0].replace('[id','')
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
            if value == None:
                nick = '{"Ник не указан"}'
                rang = '{0}'
                conf = info['peer_id'] - 2000000000
                warn = '{0}'
                cursor.execute(
                    f"""INSERT INTO "Person" VALUES(
                            '{self.id}',
                            '{nick}',
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
                f"""UPDATE "Person" SET Rang = '{{{message.split(" ")[-1]}}}'
                        WHERE "ID" = {self.id};""")
            connection.commit()
            connection.close()
            cursor.close()

