import mysql.connector
from mysql.connector import pooling
import json
import os
from dotenv import load_dotenv
from models.databaseClass import pool as p

# load_dotenv()
#
#
# MYSQL_HOST = os.getenv('MYSQL_HOST')
# MYSQL_USER = os.getenv('MYSQL_USER')
# MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
# MYSQL_DATABASE = 'movie'


class ImportDatabase:
    # def __init__(self):
    #     self.pool = pooling.MySQLConnectionPool(
    #         pool_name='pool',
    #         pool_size=5,
    #         pool_reset_session=True,
    #         host=MYSQL_HOST,
    #         database=MYSQL_DATABASE,
    #         user=MYSQL_USER,
    #         password=MYSQL_PASSWORD,
    #     )

    def add_to_database(self, movie_input):
        try:
            print('---add to database callllllll------\n')
            connection = p.get_connection()
            cursor = connection.cursor()
            cursor.execute('')
            cursor.execute('INSERT INTO movie_info VALUES(%s,%s,%s,%s,%s,%s,%s)', movie_input)
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

    def find_in_database(self, title):
        try:
            connection = p.get_connection()
            cursor = connection.cursor()
            title = title.replace('+', ' ')
            cursor.execute('SELECT id FROM movie_info WHERE title like %s', ('%'+title+'%',))
            result = cursor.fetchone()
            if result is not None:
                return True
        except Exception as e:
            print(e)
            return True
        else:
            return False
        finally:
            cursor.close()
            connection.close()

    def check_last_movie_id(self):
        try:
            connection = p.get_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT id FROM movie_info ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            print('result in check_last_movie_id-----\n', result)
            if result is None:
                return None
        except Exception as e:
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            return result
        finally:
            cursor.close()
            connection.close()


