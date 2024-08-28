import psycopg2
from config import host, user, password, db_name


class Conference:
    def __init__(self, chat_id):
        self.id = chat_id
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )

        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Conference" WHERE "ID" = {chat_id};""")
            value = cursor.fetchone()
            if value is None:
                self.hi = None
            else:
                self.hi = value[3]
                self.password = value[6]
                self.help = value[7]
                self.name = value[1]
            connection.close()
            cursor.close()

    def setHi(self, message):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE "Conference" SET htext = '{message}'
                WHERE "ID" = {self.id};""")
            connection.commit()
            self.hi = message
            connection.close()
            cursor.close()

    def setPassword(self, category_pass, passw):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE "Conference" SET pass = '{passw}'
                        WHERE "category_pass" = {category_pass};""")
            connection.commit()
            connection.close()
            cursor.close()

    def setHelp(self, id_conf, text):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE "Conference" SET help = '{text}'
                        WHERE "ID" = {id_conf};""")
            connection.commit()
            connection.close()
            cursor.close()


class ConferenceCluster:
    def __init__(self, groups=-1):
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            if groups == -1:
                cursor.execute(f"""SELECT * FROM "Conference";""")
            if groups == 0:
                cursor.execute(
                    f"""SELECT * FROM "Conference" WHERE groups[1] = 0 OR groups[2] = 0 OR groups[3] = 0 OR groups[4] = 0 OR groups[5] = 0;""")
            if groups == 1:
                cursor.execute(
                    f"""SELECT * FROM "Conference" WHERE groups[1] = 1 OR groups[2] = 1 OR groups[3] = 1 OR groups[4] = 1 OR groups[5] = 1;""")
            if groups == 2:
                cursor.execute(
                    f"""SELECT * FROM "Conference" WHERE groups[1] = 2 OR groups[2] = 2 OR groups[3] = 2 OR groups[4] = 2 OR groups[5] = 2;""")
            if groups == 3:
                cursor.execute(
                    f"""SELECT * FROM "Conference" WHERE groups[1] = 3 OR groups[2] = 3 OR groups[3] = 3 OR groups[4] = 3 OR groups[5] = 3;""")
            if groups == 4:
                cursor.execute(
                    f"""SELECT * FROM "Conference" WHERE groups[1] = 4 OR groups[2] = 4 OR groups[3] = 4 OR groups[4] = 4 OR groups[5] = 4;""")
            if groups == 5:
                cursor.execute(
                    f"""SELECT * FROM "Conference" WHERE groups[1] = 5 OR groups[2] = 5 OR groups[3] = 5 OR groups[4] = 5 OR groups[5] = 5;""")

            self.value = cursor.fetchall()
            print(self.value)


class Grp:
    def __init__(self):
        self.id = 1

    def addRecord(self, message):
        print(message)
        # connection = psycopg2.connect(
        #     host=host,
        #     user=user,
        #     password=password,
        #     database=db_name
        # )
        #
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         f"""UPDATE "Grp"
        #         SET date = '{date}',
        #         SET time = '{time}',
        #         SET info = '{info}',
        #         SET frac = '{frac}'
        #         WHERE fraction = '{fraction}';"""
        #     )
        #     connection.commit()
        #     connection.close()
        #     cursor.close()
