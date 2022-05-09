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

    # def add_to_database(self, inputs):
    #     connection = self.pool.get_connection()
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute('INSERT INTO user VALUES (%s, %s ,%s, %s)', inputs)
    #     except Exception as e:
    #         print(e)
    #         connection.rollback()
    #         return False
    #     else:
    #         connection.commit()
    #         return True
    #     finally:
    #         cursor.close()
    #         connection.close()

    # 這邊目前只搜電影 但東西一多起來就要多重考量
    def get_info(self, user_input, start_index=0):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            "select * from movieInfo where title like '%dark%'"
            cursor.execute('SELECT * FROM movieInfo Where title like %s LIMIT %s, 20', ('%'+user_input+'%', start_index))
            results = cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    # def check_user_log_in_info(self, email, password):
    #     connection = self.pool.get_connection()
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute('SELECT password,name, email, id FROM user Where email = %s', (email,))
    #         result = cursor.fetchone()
    #         hashed_password = result[0]
    #         name = result[1]
    #         email = result[2]
    #         user_id = result[3]
    #         passwords_are_the_same = bcrypt.check_password_hash(hashed_password, password)
    #         if passwords_are_the_same is not True:
    #             return False
    #     except Exception as e:
    #         print(e)
    #     else:
    #         return [name, email, user_id]
    #     finally:
    #         cursor.close()
    #         connection.close()