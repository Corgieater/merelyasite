from models.databaseClass import pool as p
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

load_dotenv()

bcrypt = Bcrypt()
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = 'movie'


class UserDatabase:
# sign up
    def add_to_database(self, inputs):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users VALUES (%s, %s ,%s, %s, DEFAULT)', inputs)
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

#拿Email
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

# check if user name taken
    def check_user_name(self, user_name):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT user_id FROM users WHERE name = %s', (user_name,))
            user_name = cursor.fetchone()
            print('user name existing? ', user_name)
            if user_name:
                result = True
                print('we have this in bank')
            else:
                result = False
                print('you can use it')
        except Exception as e:
            print(e)
        else:
            print('false')
            return result
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

# 拿user資料by name page
    def get_users_by_name(self, name, start_index):
        start_index = int(start_index) * 20
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT name, image_id FROM users WHERE name LIKE %s LIMIT %s, 20',
                           ('%' + name + '%', start_index))
            results = cursor.fetchall()

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


# show how many people are following you
    def get_user_followed_count(self, name, start_index):
        start_index = int(start_index) * 20
        print(start_index)
        print(name)
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNT(follower.following_id) as followed_by_how_many_people\n'
                           'FROM users \n'
                           'LEFT JOIN users_follows follower\n'
                           'ON follower.following_id = users.user_id\n'
                           'WHERE users.name like %s\n'
                           'GROUP BY user_id\n'
                           'LIMIT %s, 20',
                           ('%' + name + '%', start_index))
            results = cursor.fetchall()
            print(results)

        except Exception as e:
            print('get_user_followed_count userData')
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()


# show how many people you are following
    def get_user_following_count(self, name, start_index):
        start_index = int(start_index) * 20
        print(start_index)
        print(name)
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNT(follower.follower_id) as following_how_many_people\n'
                           'FROM users \n'
                           'LEFT JOIN users_follows follower\n'
                           'ON follower.follower_id = users.user_id\n'
                           'WHERE users.name like %s\n'
                           'GROUP BY user_id\n'
                           'LIMIT %s, 20\n',
                           ('%' + name + '%', start_index))
            results = cursor.fetchall()
            print(results)

        except Exception as e:
            print('get_user_following_count')
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

# get watchlist by name
    def get_watchlist(self, page_master_name, start_index):
        start_index = int(start_index)*24
        try:
            connection = p.get_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT users_watch_list.wl_movie_id\n'
                           'FROM users_watch_list\n'
                           'INNER JOIN users\n'
                           'ON users.name = %s\n'
                           'AND users.user_id = users_watch_list.wl_user_id\n'
                           'LIMIT %s,24',
                           (page_master_name,start_index))
            result = cursor.fetchall()
            print('get_watchlist', result)

        except Exception as e:
            print('get_watchlist from userData')
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()


# count watchlist by name
    def get_total_movie_in_watchlist_by_name(self, page_master):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT count(users_watch_list.wl_movie_id) as count\n'
                           'FROM users_watch_list\n'
                           'INNER JOIN users\n'
                           'ON users.name = %s\n'
                           'AND users.user_id = users_watch_list.wl_user_id\n',
                           (page_master,))
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


# check user state watchlist, likes, etc
    def check_user_state(self, user_id, content_id, type):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            if type == 'watchlist':
                cursor.execute('SELECT watch_list_id FROM users_watch_list \n'
                               'WHERE wl_user_id = %s \n'
                               'AND wl_movie_id = %s',
                               (user_id, content_id))
            if type == 'movieLikes':
                cursor.execute('SELECT mul_list_id FROM movies_users_like_list \n'
                               'WHERE mul_user_id = %s \n'
                               'AND mul_movie_id = %s',
                               (user_id, content_id))
            if type == 'reviewLikes':
                cursor.execute('SELECT rul_list_id FROM reviews_users_like_list \n'
                               'WHERE rul_user_id = %s \n'
                               'AND rul_review_id = %s',
                               (user_id, content_id))
            result = cursor.fetchone()
            print(result)
            if result is not None:
                result = True
            print('check_user_state', type, result)

        except Exception as e:
            print('check_user_state', type)
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()

# 加入待看清單 watchlist
    def add_to_watchlist(self, user_id, movie_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users_watch_list VALUES(default,%s,%s)',
                           (user_id, movie_id))
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

# delete from watchlist
    def delete_from_watchlist(self, user_id, movie_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM users_watch_list WHERE wl_user_id = %s AND wl_movie_id = %s;',
                           (user_id, movie_id))
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


# 加入movies likes
    def add_to_movies_likes(self, user_id, movie_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO movies_users_like_list VALUES(default,%s,%s, now())',
                           (user_id, movie_id))
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


# delete_from_movies_users_likes
    def delete_from_movies_users_likes(self, user_id, movie_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM movies_users_like_list WHERE mul_user_id = %s AND mul_movie_id = %s;',
                           (user_id, movie_id))
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


# 加入reviews likes
    def add_to_reviews_likes(self, user_id, review_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO reviews_users_like_list VALUES(default,%s,%s, now())',
                           (user_id, review_id))
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

# delete_from_reviews_users_likes
    def delete_from_reviews_users_likes(self, user_id, review_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM reviews_users_like_list \n'
                           'WHERE rul_user_id = %s \n'
                           'AND rul_review_id = %s',
                           (user_id, review_id))
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

# 加入user profile照片名字
    def add_user_profile_pic(self, user_id, img_name):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('UPDATE users SET image_id = %s WHERE user_id=%s',
                           (img_name, user_id))
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

    # 拿user profile 照片
    def get_user_profile_pic(self, user_name):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT image_id FROM users WHERE name = %s',
                           (user_name,))
            image_id = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        else:
            return image_id
        finally:
            cursor.close()
            connection.close()

# 拿movies user likes limit 20
    def get_movies_user_likes(self, page_master, limit_num):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT movies_users_like_list.mul_movie_id\n'
                           'FROM movies_users_like_list \n'
                           'INNER JOIN users\n'
                           'ON users.name = %s\n'
                           'AND users.user_id = mul_user_id\n'
                           'ORDER BY movies_users_like_list.mul_like_date DESC LIMIT %s',
                           (page_master, limit_num))

            image_id = cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        else:
            return image_id
        finally:
            cursor.close()
            connection.close()


# 拿reviews user likes
    def get_reviews_user_likes(self, page_master, limit_num):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT reviews_users_like_list.rul_review_id,\n'
                           'reviewer.name as reviewer, reviewer.image_id,\n'
                           'reviews.review_movie_id, reviews.movie_review, reviews.spoilers,\n'
                           'movies_info.title, movies_info.year, reviews.today\n'
                           'FROM reviews_users_like_list \n'
                           'INNER JOIN users\n'
                           'ON users.name = %s\n'
                           'AND users.user_id = rul_user_id\n'
                           'INNER JOIN reviews_users\n'
                           'INNER JOIN users reviewer\n'
                           'ON reviews_users_like_list.rul_review_id = reviews_users.reu_review_id\n'
                           'AND reviews_users.reu_user_id = reviewer.user_id\n'
                           'INNER JOIN reviews\n'
                           'INNER JOIN movies_info\n'
                           'ON reviews_users_like_list.rul_review_id = reviews.review_id\n'
                           'AND reviews.review_movie_id = movies_info.movie_id\n'
                           'ORDER BY reviews_users_like_list.rul_like_date DESC LIMIT %s',
                           (page_master, limit_num))
            image_id = cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        else:
            return image_id
        finally:
            cursor.close()
            connection.close()

# count movies user likes
    def count_all_movies_user_likes(self ,page_master):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT COUNT(movies_users_like_list.mul_movie_id)\n'
                           'FROM movies_users_like_list \n'
                           'INNER JOIN users\n'
                           'ON users.name = %s\n'
                           'AND users.user_id = movies_users_like_list.mul_user_id\n'
                           'ORDER BY movies_users_like_list.mul_like_date DESC',
                           (page_master,))
            movie_counts = cursor.fetchone()
        except Exception as e:
            print(e)
            return False
        else:
            return movie_counts
        finally:
            cursor.close()
            connection.close()