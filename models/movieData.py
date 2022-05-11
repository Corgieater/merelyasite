import os
from dotenv import load_dotenv
from mysql.connector import pooling

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
    # 拿大量資料用
    def get_info(self, user_input, start_index=0):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        start_index = int(start_index)*20
        try:
            cursor.execute('SELECT * FROM movieInfo Where title like %s LIMIT %s, 20',
                           ('%'+user_input+'%', start_index))
            results = cursor.fetchall()
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
            if result == 0:
                return None
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()

#     拿單一資料
    def get_film_by_id(self, film_id):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT * FROM movieInfo WHERE id = %s',
                           (film_id,))
            result = cursor.fetchone()
            if result is None:
                return None
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()
