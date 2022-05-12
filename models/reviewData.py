import os
from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = 'movie'


class ReviewDatabase:
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
    # 寫評論

    def write_review(self, user_review, film_id, current_date, watched_date, user_id):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO reviews VALUES (%s, %s, %s ,%s, %s ,%s)',
                           (None, user_review, film_id, current_date, watched_date, user_id))
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

    #     更新評分
    def rating(self, rate, user_id, movie_id):
        print(rate, user_id, movie_id)
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            # 找舊有無資料
            cursor.execute('SELECT * FROM rates WHERE movie_id = %s AND user_id = %s',
                           (movie_id, user_id))
            user_is_rated = cursor.fetchone()
            if user_is_rated:
                cursor.execute('UPDATE rates SET rate = %s WHERE user_id = %s AND movie_id = %s',
                               (rate, user_id, movie_id))
            else:
                cursor.execute('INSERT INTO rates VALUES (%s, %s, %s ,%s)', (None, rate, movie_id, user_id))
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

    # 拿評分資料
    def get_rate_data(self, user_id, film_id):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT rate FROM rates Where movie_id = %s AND user_id = %s',
                           (user_id, film_id))
            results = cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    # 刪除評分資料
    def delete_rate_data(self, user_id, film_id):
        connection = self.pool.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM rates WHERE movie_id = %s AND user_id = %s;',
                           (user_id, film_id))
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

    def get_total_data_count(self, user_input):
        connection = self.pool.get_connection()
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
        connection = self.pool.get_connection()
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