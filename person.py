import psycopg2
from config import host, user, password, db_name


class Person:
    def __init__(self, user_id):
        self.id = user_id
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM "Person" WHERE "ID" = {user_id};""")
            value = cursor.fetchone()
            print(value)
            self.name = value[1]
            self.nick = value[2]
            self.rang = value[3]
            self.conference = value[4]
            self.warn = value[5]
            connection.close()
            cursor.close()