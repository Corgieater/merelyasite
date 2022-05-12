import mysql.connector
from mysql.connector import pooling
import json
import os
from dotenv import load_dotenv

load_dotenv()


MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = 'movie'


class Database:
    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name='pool',
            pool_size=5,
            pool_reset_session=True,
            host=MYSQL_HOST,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
        )

    def add_to_database(self, movie_input):
        try:
            connection = self.pool.get_connection()
            connection.autocommit = False
            cursor = connection.cursor()
            cursor.execute('INSERT INTO movie_info VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', movie_input)
        except Exception as e:
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            return True
        finally:
            cursor.close()
            connection.close()


