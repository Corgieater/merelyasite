from models.databaseClass import pool as p
import os
from dotenv import load_dotenv
from mysql.connector import pooling
import flask_bcrypt as bcrypt

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = 'movie'


class UserDatabase:
    def add_to_database(self, inputs):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users VALUES (%s, %s ,%s, %s)', inputs)
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
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT email FROM users Where email = %s', (email,))
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
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT password, name, user_id FROM users Where email = %s', (email,))
            result = cursor.fetchone()
            hashed_password = result[0]
            name = result[1]
            user_id = result[2]
            # 檢查密碼
            passwords_are_the_same = bcrypt.check_password_hash(hashed_password, password)
            if passwords_are_the_same is not True:
                return False
        except Exception as e:
            print(e)
        else:
            print('user info', [name, user_id])
            return [name, user_id]
        finally:
            cursor.close()
            connection.close()

    # 算user數量 by name
    def get_total_user_count_by_name(self, user_input):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT count(*) FROM users Where name LIKE %s',
                           ('%' + user_input + '%',))
            result = cursor.fetchone()
            if result == 0:
                return None

        except Exception as e:
            print('get_total_user_count_by_name from user Data')
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()

    # 拿user資料by name page HERE 還在做
    def get_users_by_name(self, name, start_index):
        start_index = int(start_index) * 20
        print(start_index)
        print(name)
        try:
            connection = p.get_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT name FROM users WHERE name LIKE %s LIMIT %s, 20',
                           ('%' + name + '%', start_index))
            results = cursor.fetchall()
            print(results)
            print('userData get_total_user_count_by_name', len(results))
            if len(results) == 0:
                return False

            if results is None:
                return None
        except Exception as e:
            print('get_film_by_director from movieData')
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()


    # 確認使用者有沒有追蹤頁面作者
    def check_is_user_following(self, userId, page_owner):
        try:
            connection = p.get_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT\n'
                           'follower.user_id as follower_id,\n'
                           'following.user_id as following_id\n'
                           'FROM users_follows\n'
                           'INNER JOIN users following\n'
                           'ON following.name = %s\n'
                           'AND users_follows.following_id = following.user_id\n'
                           'INNER JOIN users follower\n'
                           'ON follower.user_id = %s\n'
                           'AND users_follows.follower_id = follower.user_id',
                           (page_owner, userId))
            result = cursor.fetchone()
            if len(result) == 0:
                return False
        except Exception as e:
            print('check_is_user_following from userdata')
            print(e)
            return False
        else:
            return True
        finally:
            cursor.close()
            connection.close()

    # 追蹤使用者
    def follow_other_user(self, follower_id, following_user_name):
        # find other user id and link to this user
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users_follows (following_id, follower_id)\n'
                           'SELECT following.user_id, follower.user_id\n'
                           'FROM users following, users follower\n'
                           'WHERE following.name = %s\n'
                           'And follower.user_id = %s',
                           (following_user_name, follower_id))
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