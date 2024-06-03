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
            self.hi = value[4]
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









