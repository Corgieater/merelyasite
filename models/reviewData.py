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


class ReviewDatabase:
    # 寫/更新評論
    def write_review(self, user_review, film_id, current_date, watched_date, user_id):
        connection = p.get_connection()
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

    # 刪除評論
    def delete_review(self, film_id, user_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM reviews WHERE film_id = %s AND user_id = %s;',
                           (film_id, user_id))
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

    # 拿評論 (看可不可以改寫成if else然後可以處理5或多個)
    def get_reviews_data(self, user_name):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT user.id, reviews.id, reviews.user_review, reviews.film_id, '
                           'reviews.today, reviews.watched_date, movie_info.title, movie_info.year, '
                           'rates.rate '
                           'FROM user '
                           'INNER JOIN reviews ON reviews.user_id = user.id '
                           'INNER JOIN movie_info ON reviews.film_id = movie_info.id '
                           'LEFT JOIN rates ON rates.user_id = reviews.user_id '
                           'AND rates.film_id = movie_info.id '
                           'WHERE user.name = %s '
                           'ORDER BY reviews.id DESC '
                           'LIMIT 5', (user_name,))
            results = cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    # 更新評分 先找有沒有舊的 有就更新 沒有就加入
    def rating(self, rate, user_id, movie_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT rate FROM rates WHERE film_id = %s', (movie_id,))
            result = cursor.fetchone()
            if result is not None:
                cursor.execute('INSERT INTO rates(id, rate, user_id, film_id) VALUES(%s, %s, %s, %s)',
                               (None, rate, user_id, movie_id))

            else:
                cursor.execute('UPDATE rates SET rate = %s WHERE user_id = %s AND film_id = %s',
                               (rate, user_id, movie_id,))

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
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT rate FROM rates Where film_id = %s AND user_id = %s',
                           (film_id, user_id,))
            results = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    # 刪除評分資料
    def delete_rate_data(self, film_id, user_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM rates WHERE film_id = %s AND user_id = %s;',
                           (film_id, user_id))
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

    # 拿均分資料+總共多少人平分
    def get_average_rate_data(self, film_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT count(*), ROUND(AVG(rate),1) FROM rates AS total_count WHERE film_id = %s',
                           (film_id,))
            results = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    # 算資料幾筆
    def get_total_data_count(self, user_input):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT count(*) FROM movie_info Where title LIKE %s',
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

#     用ID拿單一資料
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