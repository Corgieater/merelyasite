import os
from dotenv import load_dotenv
from mysql.connector import pooling
import flask_bcrypt as bcrypt

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = 'movie'


class MovieDatabase:
    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name='pool',
            pool_size=5,
            pool_reset_session=True,
            host=MYSQL_HOST,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )

    # 這邊目前只搜電影 但東西一多起來就要多重考量
    def get_info(self, user_input, start_index=0):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        start_index = int(start_index)*20
        try:
            cursor.execute('SELECT * FROM movieInfo Where title like %s LIMIT %s, 21',
                           ('%'+user_input+'%', start_index))
            results = cursor.fetchall()
            print(results)
        except Exception as e:
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    def get_total_data_count(self, user_input):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT count(*) FROM movieInfo Where title like %s',
                           ('%'+user_input+'%',))
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()
