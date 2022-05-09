import os
from dotenv import load_dotenv
from mysql.connector import pooling
import flask_bcrypt as bcrypt

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
            password=MYSQL_PASSWORD
        )

    def add_to_database(self, inputs):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO user VALUES (%s, %s ,%s, %s)', inputs)
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

    def get_email(self, email):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT email FROM user Where email = %s', (email,))
            result = cursor.fetchone()
            if result:
                return True
        except Exception as e:
            print(e)
        else:
            print('false')
            return False
        finally:
            cursor.close()
            connection.close()

    def check_user_log_in_info(self, email, password):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT password,name, email, id FROM user Where email = %s', (email,))
            result = cursor.fetchone()
            hashed_password = result[0]
            name = result[1]
            email = result[2]
            user_id = result[3]
            passwords_are_the_same = bcrypt.check_password_hash(hashed_password, password)
            if passwords_are_the_same is not True:
                return False
        except Exception as e:
            print(e)
        else:
            return [name, email, user_id]
        finally:
            cursor.close()
            connection.close()
