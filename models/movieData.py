from models.databaseClass import pool as p
# import os
# from dotenv import load_dotenv
# from mysql.connector import pooling
#
# load_dotenv()
#
# MYSQL_HOST = os.getenv('MYSQL_HOST')
# MYSQL_USER = os.getenv('MYSQL_USER')
# MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
# MYSQL_DATABASE = 'movie'


class MovieDatabase:
    # 這邊目前只搜電影 但東西一多起來就要多重考量
    # 無差別拿大量資料用
    def get_info(self, user_input, start_index=0):
        connection = p.get_connection()
        cursor = connection.cursor()
        start_index = int(start_index)*20
        print('user input from get info', user_input)
        try:
            cursor.execute("SELECT * FROM movie_info WHERE directors LIKE %s OR title LIKE %s "
                           "OR stars LIKE %s OR genres LIKE %s Limit %s, 20",
                           ('%'+user_input+'%', '%'+user_input+'%',
                            '%'+user_input+'%', '%'+user_input+'%', start_index))
            # cursor.execute('SELECT * FROM movie_info WHERE title LIKE %s LIMIT %s, 20 '
            #                'OR WHERE directors LIKE %s LIMIT %s, 20',
            #                ('%'+user_input+'%', start_index, '%'+user_input+'%', start_index))
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
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT count(*) FROM movie_info Where title like %s',
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
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT * FROM movie_info WHERE id = %s',
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

    # 用導演找電影
    def get_film_by_director(self, director):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT id FROM movie_info WHERE directors LIKE %s',
                           ('%'+director+'%',))
            result = cursor.fetchall()
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
