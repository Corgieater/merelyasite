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

def make_movie_info_dic(movie, directors, actors, genres):
    dic = {
        'data': {
            'movieId': movie[0],
            'title': movie[1],
            'year': movie[2],
            'story': movie[3],
            'tagline': movie[4],
            'directors': [],
            'actors': [],
            'genres': []
        }
    }
    for director in directors:
        dic['data']['directors'].append(director[0])
    for actor in actors:
        dic['data']['actors'].append(actor[0])
    for genre in genres:
        dic['data']['genres'].append(genre[0])
    return dic


def make_director_movie_dic(search_results):
    dic = {
        'data': {
            'directorID': search_results[0][0],
            'directorName': search_results[0][1],
            'directorMovieId':[]
        }
    }

    for result in search_results:
        dic['data']['directorMovieId'].append(result[2])
    return dic


def make_actor_movie_dic(search_results):
    main_dic = {
        'data':{
            'data':[]
        }
    }
    for result in search_results:
        clean_data= {
            'actorId': result[0],
            'actorName': result[1],
            'movieId': result[2]
        }
        main_dic['data']['data'].append(clean_data)
    return main_dic


class MovieDatabase:
    # 這邊目前只搜電影 但東西一多起來就要多重考量
    # 搜尋title和director+無差別拿大量資料用

    def get_info(self, user_input, start_index=0):
        # 全搜尋東西太多 只先提供電影絕對與相對名稱
        print('get_info from movieData')
        connection = p.get_connection()
        cursor = connection.cursor()
        start_index = int(start_index)*20
        print('user input from get info', user_input)
        try:
            cursor.execute('SELECT movie_id, title, year, \n'
                           'directors.name as director_name\n'
                           'FROM movies_info\n'
                           '-- INNER JOIN directors\n'
                           'INNER JOIN directors_movies\n'
                           'ON movies_info.title like %s AND \n'
                           'movies_info.movie_id = directors_movies.dm_movie_id\n'
                           'INNER JOIN directors\n'
                           'ON directors_movies.dm_director_id = directors.director_id\n'
                           'GROUP BY title\n'
                           'LIMIT %s, 20',
                           ('%'+user_input+'%', start_index))
            all_movies = cursor.fetchall()
        #     這邊或許可以擴充 如果電影<20就找導演或其他
        except Exception as e:
            print(e)
            return False
        else:
            return all_movies
        finally:
            cursor.close()
            connection.close()

    def get_total_data_count_from_type(self, user_input, input_type):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            if input_type == 'movie':
                cursor.execute('SELECT count(*) FROM movies_info Where title like %s',
                               ('%'+user_input+'%',))
                result = cursor.fetchone()
                if result == 0:
                    return None
            if input_type == 'actor':
                cursor.execute('SELECT count(*) FROM actors Where name like %s',
                               ('%' + user_input + '%',))
                result = cursor.fetchone()
                if result == 0:
                    return None
            if input_type == 'director':
                cursor.execute('SELECT COUNT(movies_info.title) AS movie_count\n'
                               'FROM directors\n'   
                               'INNER JOIN directors_movies\n'
                               'ON directors.name LIKE %s\n'
                               'AND directors.director_id = directors_movies.dm_director_id\n'
                               'INNER JOIN movies_info\n'
                               'ON directors_movies.dm_movie_id = movies_info.movie_id',
                               ('%' + user_input + '%',))
                result = cursor.fetchone()
                if result == 0:
                    return None
        except Exception as e:
            print('get_total_data_count_from_type from movie Data')
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()

#     拿單一資料 BY ID
    def get_film_by_id(self, film_id):
        try:
            connection = p.get_connection()
            cursor = connection.cursor()
            # 拿電影
            cursor.execute('SELECT * FROM movies_info WHERE movie_id = %s', (film_id,))
            movie = cursor.fetchone()
            print(movie)
            if movie is None:
                return None

            # 拿導演
            cursor.execute('SELECT directors.name\n'
                           'FROM directors_movies\n'
                           'INNER JOIN directors\n'
                           'ON directors_movies.dm_movie_id = %s\n'
                           'AND directors_movies.dm_director_id = director_id',
                           (film_id,))
            directors = cursor.fetchall()
            # 拿演員
            cursor.execute('SELECT actors.name\n'
                           'FROM actors_movies\n'
                           'INNER JOIN actors\n'
                           'ON actors_movies.am_movie_id = %s\n'
                           'AND actors_movies.am_actor_id = actor_id',
                           (film_id,))
            actors = cursor.fetchall()
            # 拿GENRE
            cursor.execute('SELECT genres.type\n'
                           'FROM genres_movies\n'
                           'INNER JOIN genres\n'
                           'ON genres_movies.gm_movie_id = %s\n'
                           'AND genres_movies.gm_movie_id = genre_id',
                           (film_id,))
            genres = cursor.fetchall()
            new_dic = make_movie_info_dic(movie, directors, actors, genres)

        except Exception as e:
            print(e)
            return False
        else:
            return new_dic
        finally:
            cursor.close()
            connection.close()

    # 用導演拿電影
    def get_film_by_director(self, director, start_index):
        start_index = int(start_index) * 20
        print(start_index)
        print(director)
        try:
            connection = p.get_connection()
            cursor = connection.cursor()
            cursor.execute('SELECT directors.director_id, directors.name,\n'
                           'directors_movies.dm_movie_id\n'
                           'FROM directors\n'
                           'INNER JOIN directors_movies\n'
                           'ON directors.name LIKE %s\n'
                           'AND directors.director_id = directors_movies.dm_director_id\n'
                           'ORDER BY director_id\n'
                           'LIMIT %s,20',
                           ('%'+director+'%', start_index))
            result = cursor.fetchall()
            print('movieData get_film_by_director', result)
            # director_id, name, movie_id
            director_movie_dic = make_director_movie_dic(result)
            if result is None:
                return None
        except Exception as e:
            print('get_film_by_director from movieData')
            print(e)
            return False
        else:
            return director_movie_dic
        finally:
            cursor.close()
            connection.close()

    # 演員拿電影(通常滿多的要LIMIT) HERE
    def get_film_by_actor(self, actor, start_index):
        start_index = int(start_index)*20
        print('movieData get_film_by_actor ', actor)
        print(type(start_index))
        try:
            connection = p.get_connection()
            cursor = connection.cursor()
            cursor.execute('''SELECT actors.actor_id, actors.name,
                                actors_movies.am_movie_id
                                FROM actors
                                INNER JOIN actors_movies
                                ON actors.name LIKE %s
                                AND actors.actor_id = actors_movies.am_actor_id
                                ORDER BY actor_id
                                LIMIT %s,20
                                ''', ('%'+actor+'%', start_index))
            result = cursor.fetchall()
            actor_movie_dic = make_actor_movie_dic(result)
            print('movieData get_film_by_actor ', result)
            if len(result) is 0:
                return None
        except Exception as e:
            print(e)
            return False
        else:
            return actor_movie_dic
        finally:
            cursor.close()
            connection.close()
