from models.databaseClass import pool as p


class ReviewDatabase:

    # 寫評論
    def write_review(self, movie_review, movie_id, current_date, watched_date, user_id, spoilers):
        connection = p.get_connection()
        cursor = connection.cursor()
        print('reviewData',movie_review, movie_id, current_date, watched_date, user_id, spoilers)
        try:
            cursor.execute('INSERT INTO reviews (review_id, review_movie_id, movie_review,'
                           'today, watched_date, spoilers)'
                           'VALUES(DEFAULT, %s, %s ,%s, %s, %s)',
                           (movie_id, movie_review, current_date, watched_date, spoilers))
            cursor.execute('SELECT LAST_INSERT_ID()')
            last_insert_review_id = cursor.fetchone()[0]
        except Exception as e:
            print('write_review reviewData')
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            self.add_relation_between_tables('reviews_users', user_id, last_insert_review_id)

        finally:
            cursor.close()
            connection.close()

    # 更新評論
    def update_review(self, review_id, movie_review, watched_date, spoilers):
        connection = p.get_connection()
        cursor = connection.cursor()
        print('update review reviewData',movie_review, watched_date, spoilers, review_id)
        try:
            cursor.execute('UPDATE reviews \n'
                           'SET \n'
                           'reviews.movie_review = %s,\n'
                           'reviews.watched_date = %s,\n'
                           'reviews.spoilers = %s\n'
                           'WHERE review_id = %s',
                           (movie_review, watched_date, spoilers, review_id,))
        except Exception as e:
            print('update_review reviewData')
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            return True

        finally:
            cursor.close()
            connection.close()

    # def add_reviews_movies_relation(self, user_id, review_id):
    #     connection = p.get_connection()
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute('INSERT INTO reviews_users (reu_id, reu_user_id, reu_review_id)\n'
    #                        'VALUES(DEFAULT, %s, %s)',
    #                        (user_id, review_id))
    #     except Exception as e:
    #         print('write_review reviewData')
    #         print(e)
    #         connection.rollback()
    #         return False
    #     else:
    #         connection.commit()
    #         return True
    #     finally:
    #         cursor.close()
    #         connection.close()



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


    # 拿單一評論by reviewId, user_name, movie_name
    def get_review_by_review_id(self, review_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT reviews.*, \n'
                           'movies_info.title, movies_info.year,\n'
                           'rates.rate\n'
                           'FROM reviews\n'
                           'INNER JOIN reviews_users\n'
                           'INNER JOIN movies_info\n'
                           'ON reviews.review_id = %s\n'
                           'AND reviews.review_id = reviews_users.reu_review_id\n'
                           'AND reviews.review_movie_id = movies_info.movie_id\n'
                           'LEFT JOIN rates\n'
                           'ON movies_info.movie_id = rates.rate_movie_id',
                           (review_id,))
            result = cursor.fetchone()
        except Exception as e:
            print('get_review_by_review_id in reviewData')
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()

    # 拿評論 (5, multiple)
    def get_reviews_data(self, user_name, page=0):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            if int(page) > 0:
                page = int(page) - 1
                start_index = int(page)*20
                cursor.execute('SELECT reviews_users.reu_review_id, \n'
                               'movies_info.title, movies_info.year,\n'
                               'reviews.*,\n'
                               'rates.rate\n'
                               'FROM users\n'
                               'INNER JOIN reviews_users\n'
                               'INNER JOIN reviews\n'
                               'ON users.name = %s\n'
                               'AND users.user_id = reviews_users.reu_user_id\n'
                               'AND reviews_users.reu_review_id = reviews.review_id\n'
                               'LEFT JOIN rates\n'
                               'ON reviews.review_movie_id = rates.rate_movie_id\n'
                               'INNER JOIN movies_info\n'
                               'ON reviews.review_movie_id = movies_info.movie_id\n'
                               'ORDER BY reviews_users.reu_id DESC\n'
                               'LIMIT %s, 20',
                               (user_name, start_index))

            else:
                cursor.execute('SELECT reviews_users.reu_review_id, \n'
                               'movies_info.title, movies_info.year,\n'
                               'reviews.*,\n'
                               'rates.rate\n'
                               'FROM users\n'
                               'INNER JOIN reviews_users\n'
                               'INNER JOIN reviews\n'
                               'ON users.name = %s\n'
                               'AND users.user_id = reviews_users.reu_user_id\n'
                               'AND reviews_users.reu_review_id = reviews.review_id\n'
                               'LEFT JOIN rates\n'
                               'ON reviews.review_movie_id = rates.rate_movie_id\n'
                               'INNER JOIN movies_info\n'
                               'ON reviews.review_movie_id = movies_info.movie_id\n'
                               'ORDER BY reviews_users.reu_id DESC\n'
                               'LIMIT 5'
                               '', (user_name,))
            results = cursor.fetchall()
            print('get_reviews_data', results)


        except Exception as e:
            print('get_reviews_data from reviewData')
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    # 更新評分 先找有沒有舊的 有就更新 沒有就加入 OK
    def rating(self, rate, user_id, film_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT rates.rate_id\n'
                           'FROM rates_users\n'
                           'INNER JOIN users\n'
                           'ON rates_users.ru_user_id = %s\n'
                           'AND rates_users.ru_user_id = users.user_id\n'
                           'INNER JOIN rates\n'
                           'ON rates_users.ru_rate_id=rates.rate_id\n'
                           'INNER JOIN movies_info\n'
                           'ON rates.rate_movie_id = %s\n'
                           'AND rates.rate_movie_id = movies_info.movie_id', (user_id, film_id))
            exist_rate_id = cursor.fetchone()
            # 這裡不能+[0] 如果是NONE會跳錯
            if exist_rate_id is None:
                cursor.execute('INSERT INTO rates(rate_id, rate, rate_movie_id) VALUES(DEFAULT, %s, %s)',
                               (rate, film_id))
                cursor.execute('SELECT LAST_INSERT_ID()')
                result = cursor.fetchone()[0]

            else:
                print('trying update')
                cursor.execute('UPDATE rates SET rate = %s WHERE rate_id = %s',
                               (rate, exist_rate_id[0]))
                result = True

        except Exception as e:
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            if result is True:
                return True
            if type(result) is int:
                # return self.add_rates_users_relation(user_id, result)
                return self.add_relation_between_tables('rates_users', user_id, result)
        finally:
            cursor.close()
            connection.close()


    # 加入關聯
    def add_relation_between_tables(self, table, first_id, second_id):
        connection = p.get_connection()
        cursor = connection.cursor()

        try:
            # 關聯兩張表
            if table == 'rates_users':
                cursor.execute('INSERT INTO rates_users VALUES(DEFAULT, %s, %s)',
                               (first_id, second_id))
            if table == 'reviews_users':
                cursor.execute('INSERT INTO reviews_users VALUES(DEFAULT, %s, %s)',
                               (first_id, second_id))

        except Exception as e:
            print('add_relation_between_tables reviewData')
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
            cursor.execute('SELECT rates.rate_id, rates.rate, movies_info.title\n'
                           'FROM rates_users\n'
                           'INNER JOIN users\n'
                           'ON rates_users.ru_user_id = %s\n'
                           'AND rates_users.ru_user_id = users.user_id\n'
                           'INNER JOIN rates\n'
                           'ON rates_users.ru_rate_id=rates.rate_id\n'
                           'INNER JOIN movies_info\n'
                           'ON rates.rate_movie_id = %s\n'
                           'AND rates.rate_movie_id = movies_info.movie_id;\n'
                           '            ',
                           (user_id, film_id))
            results = cursor.fetchone()[1]
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
        try:
            cursor.execute('SELECT rates.rate_id\n'
                           'FROM rates\n'
                           'INNER join rates_users\n'
                           'ON rates_users.ru_user_id = %s\n'
                           'AND rates.rate_movie_id = %s\n'
                           'AND rates_users.ru_rate_id = rates.rate_id;',
                           (user_id, film_id))
            rate_id = cursor.fetchone()[0]
            cursor.execute('DELETE FROM rates WHERE rate_id = %s', (rate_id,))

        except Exception as e:
            print('delete rate data from reviewData')
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
            cursor.execute('SELECT count(*), ROUND(AVG(rate),1) FROM rates AS total_count WHERE rate_movie_id = %s',
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

    def get_user_reviews_count(self, user_name):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT count(users.name) as review_count\n'
                           'FROM users\n'
                           'INNER JOIN reviews_users\n'
                           'ON users.name = %s\n'
                           'AND reviews_users.reu_user_id = users.user_id', (user_name,))
            results = cursor.fetchone()
            print(results, 'from get_user_reviews_count')
        except Exception as e:
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    # 算資料幾筆
    # def get_total_data_count(self, user_input):
    #     connection = p.get_connection()
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute('SELECT count(*) FROM movies_info Where title LIKE %s',
    #                        ('%'+user_input+'%',))
    #         result = cursor.fetchone()
    #         if result == 0:
    #             return None
    #     except Exception as e:
    #         print(e)
    #         return False
    #     else:
    #         return result
    #     finally:
    #         cursor.close()
    #         connection.close()

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
