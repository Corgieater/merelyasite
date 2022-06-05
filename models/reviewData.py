from models.databaseClass import pool as p


class ReviewDatabase:

    # 寫評論
    def write_review(self, movie_review, movie_id, current_date, watched_date, user_id, spoilers):
        connection = p.get_connection()
        cursor = connection.cursor()
        print('wrtie review from reviewData, movie_review, movie_id, current_date, watched_date, user_id, spoilers')
        print(movie_review, movie_id, current_date, watched_date, user_id, spoilers)
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
            print('write_review add review sucess try adding relation')
            add_relation = self.add_relation_between_tables('reviews_users', user_id, last_insert_review_id)
            if add_relation:
                return True
            else:
                print('write_review review data add relation failed')
                return False

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


    # 刪除評論
    def delete_review(self, review_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('''DELETE FROM reviews WHERE review_id = %s''',
                           (review_id,))
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


    # 拿單一評論by reviewId, user_name, movie_name HERE WATCHING
    def get_review_by_review_id(self, review_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        print('reviewdata get review by review id',review_id)
        try:
            cursor.execute('SELECT reviews.*,reviews_users.reu_user_id,\n'
                           'movies_info.title, movies_info.year\n'
                           'FROM reviews\n'
                           'INNER JOIN reviews_users\n'
                           'INNER JOIN movies_info\n'
                           'ON reviews.review_id = %s\n'
                           'AND reviews.review_id = reviews_users.reu_review_id\n'
                           'AND reviews.review_movie_id = movies_info.movie_id',
                           (review_id,))
            review_result = cursor.fetchone()
            print('get_review_by_review_id', review_result)
            user_id = review_result[6]
            movie_id = review_result[1]
            cursor.execute('select rates.rate\n'
                           'from rates\n'
                           'inner join rates_users\n'
                           'on rates_users.ru_user_id = %s\n'
                           'and rates.rate_movie_id = %s\n'
                           'and rates_users.ru_rate_id = rates.rate_id',
                           (user_id, movie_id))
            rate_result = cursor.fetchone()
            print('rate_result',rate_result)
            final_result = [review_result, rate_result]
            # cursor.execute('SELECT reviews.*,\n'
            #                'movies_info.title, movies_info.year,\n'
            #                'rates.rate\n'
            #                'FROM reviews\n'
            #                'INNER JOIN reviews_users\n'
            #                'INNER JOIN movies_info\n'
            #                'ON reviews.review_id = %s\n'
            #                'AND reviews.review_id = reviews_users.reu_review_id\n'
            #                'AND reviews.review_movie_id = movies_info.movie_id\n'
            #                'LEFT JOIN rates_users\n'
            #                'on rates_users.ru_user_id = reviews_users.reu_user_id\n'
            #                'INNER JOIN rates\n'
            #                'ON movies_info.movie_id = rates.rate_movie_id\n'
            #                'AND rates_users.ru_rate_id = rates.rate_id',
            #                (review_id,))
            # cursor.execute('SELECT reviews.*,\n'
            #                'movies_info.title, movies_info.year,\n'
            #                'rates.rate\n'
            #                'from users\n'
            #                'inner join reviews\n'
            #                'inner join movies_info\n'
            #                'on users.name = %s\n'
            #                'and reviews.review_id = %s\n'
            #                'and reviews.review_movie_id = movies_info.movie_id\n'
            #                'left join rates\n'
            #                'on rates.rate_movie_id = reviews.review_movie_id\n'
            #                'left join rates_users\n'
            #                'on rates_users.ru_user_id = users.user_id\n'
            #                'and rates_users.ru_rate_id = rates.rate_id',
            #                (page_master_name, review_id))

            # cursor.execute('SELECT reviews.*, \n'
            #                'movies_info.title, movies_info.year,\n'
            #                'rates.rate\n'
            #                'FROM reviews\n'
            #                'INNER JOIN reviews_users\n'
            #                'INNER JOIN movies_info\n'
            #                'ON reviews.review_id = %s\n'
            #                'AND reviews.review_id = reviews_users.reu_review_id\n'
            #                'AND reviews.review_movie_id = movies_info.movie_id\n'
            #                'LEFT JOIN rates\n'
            #                'ON movies_info.movie_id = rates.rate_movie_id',
            #                (review_id,))

        except Exception as e:
            print('get_review_by_review_id in reviewData')
            print(e)
            return False
        else:
            return final_result
        finally:
            cursor.close()
            connection.close()

    # 拿評論 (5, multiple) 整個拿profile評論都有問題?? WATCHING FIXED? 怎麼拿評分?
    def get_reviews_data(self, user_name, page=0):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            if int(page) > 0:
                page = int(page) - 1
                start_index = int(page)*20
                # 選不到評分 分開看看
                cursor.execute('SELECT movies_info.title, movies_info.year, reviews.*\n'
                               'FROM users\n'
                               'INNER JOIN reviews_users\n'
                               'ON users.name = %s\n'
                               'AND users.user_id = reviews_users.reu_user_id\n'
                               'INNER JOIN reviews\n'
                               'ON reviews.review_id = reviews_users.reu_review_id\n'
                               'INNER JOIN movies_info\n'
                               'ON reviews.review_movie_id = movies_info.movie_id\n'
                               'ORDER BY reviews.review_id DESC\n'
                               'LIMIT %s, 20', (user_name, start_index))

                # 選得到評分 選不到沒評分的片 幹
                # cursor.execute('SELECT\n'
                #                'movies_info.title, movies_info.year,\n'
                #                'reviews.*,\n'
                #                'rates.rate\n'
                #                'FROM reviews_users\n'
                #                'INNER JOIN users\n'
                #                'INNER JOIN reviews\n'
                #                'INNER JOIN movies_info\n'
                #                'ON users.name = %s\n'
                #                'AND users.user_id = reviews_users.reu_user_id\n'
                #                'AND reviews_users.reu_review_id = reviews.review_id\n'
                #                'AND movies_info.movie_id = reviews.review_movie_id\n'
                #                'LEFT join rates_users\n'
                #                'ON rates_users.ru_user_id = reviews_users.reu_user_id\n'
                #                'INNER JOIN rates\n'
                #                'ON rates.rate_movie_id = movies_info.movie_id\n'
                #                'AND rates_users.ru_rate_id = rates.rate_id\n'
                #                'ORDER BY reviews.review_id DESC\n'
                #                'LIMIT %s, 20',
                #                (user_name, start_index))

            else:
                cursor.execute('SELECT movies_info.title, movies_info.year, reviews.*, users.user_id\n'
                               'FROM users\n'
                               'INNER JOIN reviews_users\n'
                               'ON users.name = %s\n'
                               'AND users.user_id = reviews_users.reu_user_id\n'
                               'INNER JOIN reviews\n'
                               'ON reviews.review_id = reviews_users.reu_review_id\n'
                               'INNER JOIN movies_info\n'
                               'ON reviews.review_movie_id = movies_info.movie_id\n'
                               'ORDER BY reviews.review_id DESC\n'
                               'LIMIT 5', (user_name,))



                # cursor.execute('SELECT\n'
                #                'movies_info.title, movies_info.year,\n'
                #                'reviews.*,\n'
                #                'rates.rate\n'
                #                'FROM reviews_users\n'
                #                'INNER JOIN users\n'
                #                'INNER JOIN reviews\n'
                #                'INNER JOIN movies_info\n'
                #                'ON users.name = %s\n'
                #                'AND users.user_id = reviews_users.reu_user_id\n'
                #                'AND reviews_users.reu_review_id = reviews.review_id\n'
                #                'AND movies_info.movie_id = reviews.review_movie_id\n'
                #                'LEFT join rates_users\n'
                #                'ON rates_users.ru_user_id = reviews_users.reu_user_id\n'
                #                'INNER JOIN rates\n'
                #                'ON rates.rate_movie_id = movies_info.movie_id\n'
                #                'AND rates_users.ru_rate_id = rates.rate_id\n'
                #                'ORDER BY reviews.review_id DESC\n'
                #                'LIMIT 5'
                #                , (user_name,))
            results = cursor.fetchall()

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
                print('trying insert rating')
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
                print('relation between rates_users')
                cursor.execute('INSERT INTO rates_users VALUES(DEFAULT, %s, %s)',
                               (first_id, second_id))
            if table == 'reviews_users':
                print('relation between reviews_users')
                cursor.execute('INSERT INTO reviews_users VALUES(DEFAULT, %s, %s)',
                               (first_id, second_id))

        except Exception as e:
            print('add_relation_between_tables reviewData')
            print('add_relation_between_tables reviewData fail')
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            print('add_relation_between_tables reviewData success')
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
                           'AND rates.rate_movie_id = movies_info.movie_id\n',
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

    #  算使用者REVIEWS有幾篇 by name
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

    # #  從REVIEW ID拿到電影跟使用者ID
    # #  給從USER PROFILE REVIEW AGAIN用
    def get_movie_id_and_user_id_for_review_again(self, review_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT reviews.review_movie_id, reviews_users.reu_user_id\n'
                           'FROM reviews\n'
                           'INNER JOIN reviews_users\n'
                           'ON reviews.review_id = %s\n'
                           'AND reviews.review_id = reviews_users.reu_review_id',
                           (review_id,))
            results = cursor.fetchone()
            print(results, 'get_movie_id_and_user_id_for_review_again')
        except Exception as e:
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()


    # 用使用者追蹤的對象拿review
    def get_latest_five_reviews_from_follows(self, user_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT users.name,\n'
                           'reviews.review_id, reviews.review_movie_id,reviews.today,\n'
                           'movies_info.title\n'
                           'FROM users_follows\n'
                           'INNER JOIN reviews_users\n'
                           'INNER JOIN reviews\n'
                           'INNER JOIN users\n'
                           'INNER JOIN movies_info\n'
                           'ON users_follows.follower_id = %s\n'
                           'AND users_follows.following_id = reviews_users.reu_user_id\n'
                           'AND reviews_users.reu_review_id = reviews.review_id\n'
                           'AND reviews.review_movie_id = movies_info.movie_id\n'
                           'AND users_follows.following_id = users.user_id\n'
                           'ORDER BY reviews.review_id DESC\n'
                           'LIMIT 6',
                           (user_id,))
            results = cursor.fetchall()
            print('get_latest_five_reviews_from_follows', results)
        except Exception as e:
            print('get_latest_five_reviews_from_follows from reviewData')
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()


    # 拿12篇評論給index
    def get_latest_reviews_for_index(self):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT \n'
                           'users.name,\n'
                           'movies_info.title,\n'
                           'reu_review_id,\n'
                           'reviews.review_movie_id\n'
                           'FROM reviews_users\n'
                           'INNER JOIN reviews\n'
                           'INNER JOIN users\n'
                           'INNER JOIN movies_info\n'
                           'ON reviews_users.reu_user_id = users.user_id\n'
                           'AND reviews_users.reu_review_id = reviews.review_id\n'
                           'AND movies_info.movie_id = reviews.review_movie_id\n'
                           'ORDER BY reu_id DESC LIMIT 11')
            results = cursor.fetchall()
            print('get_latest_reviews_for_index', results)
        except Exception as e:
            print('get_latest_reviews_for_index from reviewData')
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()

    # count all reviews
    def get_all_reviews_count(self):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNT(review_id)AS count FROM reviews')
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()

    # 算review搜尋有多少筆資料 HERE 這裡有問題 會找到沒review的電影
    def get_total_review_count_by_title_and_content(self, review_query):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNT(*) \n'
                           'FROM(\n'
                           'SELECT movies_info.title\n'
                           'FROM movies_info\n'
                           'WHERE movies_info.title like %s\n'
                           'UNION\n'
                           'SELECT reviews.movie_review\n'
                           'FROM reviews\n'
                           'WHERE reviews.movie_review like %s\n'
                           ') content\n', ('%'+review_query+'%', '%'+review_query+'%'))
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()


    # 拿movie title, review content有包含user做review搜尋的資料
    def get_review_by_title_and_content(self, review_query, start_point):
        connection = p.get_connection()
        cursor = connection.cursor()
        start_point = int(start_point)*20
        try:
            cursor.execute('SELECT movie_id, title, year,\n'
                           'review_id, movie_review, spoilers\n'
                           ',reviews_users.reu_user_id,\n'
                           'users.name\n'
                           'FROM movies_info\n'
                           'INNER JOIN reviews\n'
                           'ON movies_info.title like %s\n'
                           'AND reviews.review_movie_id = movies_info.movie_id\n'
                           'INNER JOIN reviews_users\n'
                           'ON reviews.review_id = reviews_users.reu_review_id\n'
                           'INNER JOIN users\n'
                           'ON reviews_users.reu_user_id = users.user_id\n'
                           'UNION\n'
                           'SELECT movie_id, title, year,\n'
                           'review_id, movie_review, spoilers\n'
                           ',reviews_users.reu_user_id,\n'
                           'users.name\n'
                           'FROM movies_info\n'
                           'INNER JOIN reviews\n'
                           'ON reviews.movie_review like %s\n'
                           'AND reviews.review_movie_id = movies_info.movie_id\n'
                           'INNER JOIN reviews_users\n'
                           'ON reviews.review_id = reviews_users.reu_review_id\n'
                           'INNER JOIN users\n'
                           'ON reviews_users.reu_user_id = users.user_id\n'
                           'GROUP BY review_id\n'
                           'LIMIT %s, 20', ('%'+review_query+'%', '%'+review_query+'%', start_point))
            result = cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()


# 拿多少人like this review
    def get_total_review_likes(self, review_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNT(*) \n'
                           'FROM(\n'
                           'SELECT rul_review_id\n'
                           'FROM reviews_users_like_list\n'
                           'WHERE rul_review_id = %s\n'
                           ') content', (review_id,))
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()


    # 拿追蹤的人最近喜歡了什麼評論*4 for index HERE
    def get_followings_like_reviews(self, user_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT\n'
                           'reviews_users_like_list.rul_review_id,\n'
                           'reviews.review_movie_id, reviews.movie_review, \n'
                           'reviews.spoilers, movies_info.title,\n'
                           'u.name as reviewer\n'
                           'from users_follows \n'
                           'INNER JOIN reviews_users_like_list\n'
                           'ON follower_id = %s\n'
                           'AND following_id = reviews_users_like_list.rul_user_id\n'
                           'INNER JOIN reviews\n'
                           'INNER JOIN movies_info\n'
                           'INNER JOIN users\n'
                           'ON following_id = users.user_id\n'
                           'AND reviews_users_like_list.rul_review_id=reviews.review_id\n'
                           'AND reviews.review_movie_id = movies_info.movie_id\n'
                           'INNER JOIN users u\n'
                           'INNER JOIN reviews_users\n'
                           'ON reviews.review_id = reviews_users.reu_review_id\n'
                           'AND reviews_users.reu_user_id = u.user_id\n'
                           'GROUP BY reviews_users_like_list.rul_review_id\n'
                           'ORDER BY reviews_users_like_list.rul_review_id DESC\n'
                           'LIMIT 4', (user_id,))
            result = cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()


    # get most popular reviews*4 for index HERE
    def get_most_popular_reviews(self):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT\n'
                           'reviews.review_id, reviews.movie_review ,reviews.review_movie_id,\n'
                           'reviews.spoilers,\n'
                           'movies_info.title,\n'
                           'users.name,\n'
                           'COUNT(rul_review_id) AS occurrence\n'
                           'FROM\n'
                           'reviews_users_like_list\n'
                           'INNER JOIN reviews\n'
                           'INNER JOIN movies_info\n'
                           'INNER JOIN reviews_users\n'
                           'INNER JOIN users\n'
                           'ON reviews.review_id = reviews_users_like_list.rul_review_id\n'
                           'AND reviews.review_movie_id = movies_info.movie_id\n'
                           'AND reviews_users.reu_review_id = reviews.review_id\n'
                           'AND reviews_users.reu_user_id = users.user_id\n'
                           'GROUP BY rul_review_id\n'
                           'ORDER BY occurrence DESC\n'
                           'LIMIT 4;')
            result = cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()
