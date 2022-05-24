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
    # 寫/更新評論 renew not yet done
    def write_review(self, user_review, movie_id, current_date, watched_date, user_id, spoilers):
        connection = p.get_connection()
        cursor = connection.cursor()
        print('reviewData',user_review, movie_id, current_date, watched_date, user_id, spoilers)
        try:
            cursor.execute('INSERT INTO reviews (review_id, user_review,'
                           'movie_id, today, watched_date, user_id, spoilers)'
                           'VALUES(DEFAULT, %s, %s ,%s, %s, %s, %s)',
                           (user_review, movie_id, current_date, watched_date, user_id, spoilers))
        except Exception as e:
            print('write_review reviewData')
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
            cursor.execute('SELECT reviews.user_review, reviews.today, reviews.watched_date,\n'
                           'reviews.review_id, reviews.spoilers,\n'
                           'movies_info.movie_id, movies_info.title, movies_info.year,\n'
                           'rates.rate\n'
                           'FROM users\n'
                           'INNER JOIN reviews\n'
                           'ON users.name = %s\n'
                           'AND users.user_id = reviews.user_id\n'
                           'INNER JOIN movies_info \n'
                           'ON reviews.movie_id = movies_info.movie_id\n'
                           'LEFT JOIN rates\n'
                           'ON users.user_id = rates.rate_user_id\n'
                           'AND reviews.movie_id = rates.rate_film_id\n'
                           'ORDER BY review_id DESC\n'
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

    # 更新評分 先找有沒有舊的 有就更新 沒有就加入 OK
    def rating(self, rate, user_id, film_id):
        print('reviewData rating')
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            print('trying finding')
            cursor.execute('SELECT rate FROM rates WHERE rate_film_id = %s AND rate_user_id = %s', (film_id, user_id))
            result = cursor.fetchone()
            print(result)
            if result is None:
                print('trying insert')
                cursor.execute('INSERT INTO rates(rate_id, rate, rate_user_id, rate_film_id) VALUES(%s, %s, %s, %s)',
                               (None, rate, user_id, film_id))
            else:
                print('trying update')
                cursor.execute('UPDATE rates SET rate = %s WHERE rate_user_id = %s AND rate_film_id = %s',
                               (rate, user_id, film_id,))

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

    # 拿評分資料 OK
    def get_rate_data(self, user_id, film_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT rate FROM rates Where rate_film_id = %s AND rate_user_id = %s',
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

    # 刪除評分資料 OK
    def delete_rate_data(self, film_id, user_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        print('in delete rate data from reviewData')
        try:
            cursor.execute('DELETE FROM rates WHERE rate_film_id = %s AND rate_user_id = %s',
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

    # 拿均分資料+總共多少人平分 OK
    def get_average_rate_data(self, film_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT count(*), ROUND(AVG(rate),1) FROM rates AS total_count WHERE rate_film_id = %s',
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
            cursor.execute('SELECT count(*) FROM movies_info Where title LIKE %s',
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

#     用ID拿單一資料 看起來沒用
#     def get_film_by_id(self, film_id):
#         connection = p.get_connection()
#         cursor = connection.cursor()
#         try:
#             cursor.execute('SELECT * FROM movies_info WHERE id = %s',
#                            (film_id,))
#             result = cursor.fetchone()
#             if result is None:
#                 return None
#         except Exception as e:
#             print(e)
#             return False
#         else:
#             return result
#         finally:
#             cursor.close()
#             connection.close()
