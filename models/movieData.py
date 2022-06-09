from models.databaseClass import pool as p

# 給詳細單頁Movie用的
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


# 做general search後面的秀海報頁面(導演演員)
def make_poster_showing_dic(search_results, data_type):
    dic = {
        'data': {
            f'{data_type}ID': search_results[0][0],
            f'{data_type}Name': search_results[0][1],
            f'{data_type}MovieId': []
        }
    }

    for result in search_results:
        dic['data'][f'{data_type}MovieId'].append(result[2])
    return dic


# 做導演演員DIC含幾部作品 GENERAL搜尋bar
def make_dic_by_type_for_general_search(search_results, movie_counts_list, data_type):
    main_dic = {
        'data': {
            'data': []
        }
    }
    for result in search_results:
        clean_data = {
            f'{data_type}Id': result[0],
            f'{data_type}Name': result[1],
            f'{data_type}MovieCount': None
        }
        main_dic['data']['data'].append(clean_data)
    for i in range(len(search_results)):
        main_dic['data']['data'][i][f'{data_type}MovieCount'] = movie_counts_list[i]
    return main_dic


class MovieDatabase:
# 拿電影資料
    def get_movie_info_by_keyword(self, user_input, start_index=0):
        connection = p.get_connection()
        cursor = connection.cursor()
        start_index = int(start_index)*20
        try:
            cursor.execute('SELECT movie_id, title, year, \n'
                           'directors.name as director_name\n'
                           'FROM movies_info\n'
                           'INNER JOIN directors_movies\n'
                           'ON movies_info.title like %s AND \n'
                           'movies_info.movie_id = directors_movies.dm_movie_id\n'
                           'INNER JOIN directors\n'
                           'ON directors_movies.dm_director_id = directors.director_id\n'
                           'GROUP BY title\n'
                           'LIMIT %s, 20',
                           ('%'+user_input+'%', start_index))
            all_movies = cursor.fetchall()

        except Exception as e:
            print('get_info from movieData')
            print(e)
            return False
        else:
            return all_movies
        finally:
            cursor.close()
            connection.close()

# 算資料數量 by input type
    def get_total_data_count_from_type(self, user_input, input_type):
        connection = p.get_connection()
        cursor = connection.cursor()
        result = None
        try:
            if input_type == 'movie':
                cursor.execute('SELECT count(*) FROM movies_info Where title LIKE %s',
                               ('%'+user_input+'%',))
                result = cursor.fetchone()

            # 算actor人名有幾個差不多的
            if input_type == 'actor':
                cursor.execute('SELECT count(*) FROM actors Where name like %s',
                               ('%' + user_input + '%',))
                result = cursor.fetchone()

            # 算導演人名有幾個差不多的
            if input_type == 'director':
                cursor.execute('''SELECT COUNT(*) FROM directors WHERE name LIKE %s''',
                               ('%' + user_input + '%',))
                result = cursor.fetchone()

            if input_type == 'genre':
                cursor.execute('select count(movies_info.title) as count\n'
                               'from genres\n'
                               'inner join genres_movies \n'
                               'ON genres.type like %s\n'
                               'AND genres.genre_id = genres_movies.gm_genre_id\n'
                               'inner join movies_info\n'
                               'ON genres_movies.gm_movie_id = movies_info.movie_id\n',
                               ('%' + user_input + '%',))
                result = cursor.fetchone()

            # 算導演拍幾部電影
            if input_type == 'director_movies':
                cursor.execute('SELECT COUNT(directors_movies.dm_director_id) AS movie_count\n'
                               'FROM directors\n'
                               'INNER JOIN directors_movies\n'
                               'ON directors.name LIKE %s\n'
                               'AND directors.director_id = directors_movies.dm_director_id\n',
                               ('%' + user_input + '%',))
                result = cursor.fetchone()

            # 算演員拍幾部電影
            if input_type == 'actor_movies':
                cursor.execute('SELECT COUNT(actors_movies.am_actor_id) AS movie_count\n'
                               'FROM actors\n'
                               'INNER JOIN actors_movies\n'
                               'ON actors.name LIKE %s\n'
                               'AND actors.actor_id = actors_movies.am_actor_id',
                               ('%' + user_input + '%',))
                result = cursor.fetchone()

        except Exception as e:
            print('get_total_data_count_from_type from movie Data')
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()

# 拿單一電影 BY ID
    def get_film_by_id(self, film_id):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
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
                           'AND genres_movies.gm_genre_id = genres.genre_id ',
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
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
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
            if len(result) == 0:
                return False
            # director_id, name, movie_id
            director_movie_dic = make_poster_showing_dic(result, 'director')
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

# 演員拿電影
    def get_film_by_actor(self, actor, start_index):
        start_index = int(start_index)*20
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT actors.actor_id, actors.name,\n'
                           'actors_movies.am_movie_id\n'
                           'FROM actors\n'
                           'INNER JOIN actors_movies\n'
                           'ON actors.name LIKE %s\n'
                           'AND actors.actor_id = actors_movies.am_actor_id\n'
                           'ORDER BY actor_id\n'
                           'LIMIT %s,20\n', ('%' + actor + '%', start_index))
            result = cursor.fetchall()
            actor_movie_dic = make_poster_showing_dic(result, 'actor')
            if len(result) == 0:
                return None
        except Exception as e:
            print(e)
            return False
        else:
            return actor_movie_dic
        finally:
            cursor.close()
            connection.close()

    # GENRE拿電影 director(通常滿多的要LIMIT)
    def get_film_by_genre(self, genre, start_index):
        start_index = int(start_index) * 20
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT movies_info.movie_id,movies_info.title,\n'
                           'movies_info.year, directors.name\n'
                           'FROM genres\n'
                           'INNER JOIN genres_movies\n'
                           'INNER JOIN movies_info\n'
                           'INNER JOIN directors_movies\n'
                           'INNER JOIN directors\n'
                           'ON genres.type like %s\n'
                           'AND genres_movies.gm_genre_id = genres.genre_id\n'
                           'AND genres_movies.gm_movie_id = movies_info.movie_id\n'
                           'AND directors_movies.dm_movie_id = movies_info.movie_id\n'
                           'AND directors_movies.dm_director_id = directors.director_id\n'
                           'GROUP BY movies_info.title\n'
                           'LIMIT %s, 20',
                           ('%' + genre + '%', start_index))
            result = cursor.fetchall()
            if len(result) == 0:
                return None
        except Exception as e:
            print('get_film_by_genre from movieData')
            print(e)
            return False
        else:
            return result
        finally:
            cursor.close()
            connection.close()

    # general搜尋bar 名字拿導演
    def get_director_by_name(self, director, page, total_count):
        start_index = int(page) * 20
        if start_index > total_count:
            start_index = (int(page)-1)*20+1

        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT directors.director_id, directors.name\n'
                           'FROM directors\n'
                           'INNER JOIN directors_movies\n'
                           'ON directors.name LIKE %s\n'
                           'AND directors.director_id = directors_movies.dm_director_id\n'
                           'INNER JOIN movies_info\n'
                           'ON directors_movies.dm_movie_id = movies_info.movie_id\n'
                           'GROUP BY director_id\n'
                           'ORDER BY name\n'
                           'LIMIT %s, 20',
                           ('%' + director + '%', start_index))
            result = cursor.fetchall()
            movie_counts = []
            for director_id in result:
                cursor.execute('SELECT COUNT(*) FROM directors_movies WHERE dm_director_id =%s',
                               (director_id[0],))
                movie_counts.append(cursor.fetchone()[0])
            general_search_dic = make_dic_by_type_for_general_search(result, movie_counts, 'director')
            if len(result) == 0:
                return None
        except Exception as e:
            print('get_director_by_name from movieData')
            print(e)
            return False
        else:
            return general_search_dic
        finally:
            cursor.close()
            connection.close()

    # general搜尋bar 名字拿演員
    def get_actor_by_name(self, actor, page, total_count):
        start_index = int(page) * 20
        if start_index > total_count:
            start_index = (int(page) - 1) * 20 + 1
        print(start_index)
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT actors.actor_id, actors.name,\n'
                           'actors_movies.am_movie_id\n'
                           'FROM actors\n'
                           'INNER JOIN actors_movies\n'
                           'ON actors.name like %s \n'
                           'AND actors.actor_id = actors_movies.am_actor_id\n'
                           'GROUP BY actor_id\n'
                           'ORDER BY name\n'
                           'LIMIT %s,20', ('%'+actor+'%', start_index))
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                return False
            movie_counts = []
            for actor_id in result:
                cursor.execute('SELECT COUNT(*) FROM actors_movies WHERE am_actor_id =%s',
                               (actor_id[0],))
                movie_counts.append(cursor.fetchone()[0])
            general_search_dic = make_dic_by_type_for_general_search(result, movie_counts, "actor")
            if len(result) == 0:
                return False
        except Exception as e:
            print('get_actor_by_name from movieData')
            print(e)
            return False
        else:
            return general_search_dic
        finally:
            cursor.close()
            connection.close()

    # 拿這禮拜最多人按讚的電影 by 6
    def get_most_popular_movies_for_index(self):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT mul_movie_id, COUNT(*) as popularity\n'
                           'FROM movies_users_like_list \n'
                           'WHERE YEARWEEK(mul_like_date) = YEARWEEK(NOW())\n'
                           'GROUP BY mul_movie_id\n'
                           'ORDER BY popularity DESC\n'
                           'LIMIT 6')
            results = cursor.fetchall()

        except Exception as e:
            print('get_most_popular_movie_this_week')
            print(e)
            return False
        else:
            return results
        finally:
            cursor.close()
            connection.close()
