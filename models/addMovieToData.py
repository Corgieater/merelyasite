from models.movieData import *
import random
import time


def random_delay(time_list):
    delay_choices = time_list
    delay = random.choice(delay_choices)
    time.sleep(delay)


class ImportDatabase:
    def add_movie_to_database(self, movie_info):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO movies_info(movie_id, title, year, story_line, tagline)'
                           ' VALUES(DEFAULT,%s,%s,%s,%s)',
                           (movie_info[0], movie_info[1], movie_info[2], movie_info[3]))
            cursor.execute('SELECT LAST_INSERT_ID()')

            last_insert_movie_id = cursor.fetchone()[0]

        except Exception as e:
            print('add_to_database from addMovieToData got problem',)
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            return last_insert_movie_id
        finally:
            cursor.close()
            connection.close()

# title and year for search movie
    def find_movie_in_database(self, title, year):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            title = title.replace('+', ' ')
            cursor.execute('SELECT movie_id FROM movies_info WHERE title like %s and year = %s', ('%'+title+'%', year))
            result = cursor.fetchone()
            if result is not None:
                return True
        except Exception as e:
            print(e)
            return True
        else:
            return False
        finally:
            cursor.close()
            connection.close()

# GENRE添加
    def add_genre_to_database(self, genre):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('')
            cursor.execute('INSERT INTO genres(genre_id, type) '
                           'VALUES(DEFAULT,%s)', (genre,))
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

 # 添加導演
    def add_director_to_database(self, director):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('')
            cursor.execute('INSERT INTO directors(director_id, name) '
                           'VALUES(DEFAULT,%s)', (director,))
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

# 添加演員
    def add_acotor_to_database(self, actor):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO actors(actor_id, name) '
                           'VALUES(DEFAULT,%s)', (actor,))
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

# 添加關聯by type
    def add_relationship(self, input_tuple, input_type):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            if input_type == 'director':
                cursor.execute('INSERT INTO directors_movies(dm_id, dm_director_id, dm_movie_id) '
                               'VALUES(DEFAULT, %s, %s)', input_tuple)
            if input_type == 'actor':
                cursor.execute('INSERT INTO actors_movies(am_id, am_actor_id, am_movie_id) '
                               'VALUES(DEFAULT, %s, %s)', input_tuple)
            if input_type == 'genre':
                cursor.execute('INSERT INTO genres_movies(gm_id, gm_genre_id, gm_movie_id) '
                               'VALUES(DEFAULT, %s, %s)', input_tuple)
        except Exception as e:
            print('add_relationship', input_tuple)
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            return True
        finally:
            cursor.close()
            connection.close()

# 多功能搜尋
    def find_input_from_table(self, id_type, table, column, input_content):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(f'SELECT {id_type} FROM {table} WHERE {column} = %s', (input_content,))
            input_id = cursor.fetchone()
            if input_id is not None:
                input_id = input_id[0]
        except Exception as e:
            print('find_input_from_table from addMovietodata', id_type)
            print(e)
            return False
        else:
            return input_id
        finally:
            cursor.close()
            connection.close()

# 多功能添加
    def add_subject_to_database_by_type(self, subject, input_type):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            if input_type == 'director':
                cursor.execute('INSERT INTO directors(director_id, name) '
                               'VALUES(DEFAULT,%s)', (subject,))
            if input_type == 'actor':
                cursor.execute('INSERT INTO actors(actor_id, name) '
                               'VALUES(DEFAULT,%s)', (subject,))
            if input_type == 'genre':
                cursor.execute('INSERT INTO genres(genre_id, type) '
                               'VALUES(DEFAULT,%s)', (subject,))
            cursor.execute('SELECT LAST_INSERT_ID()')
            result = cursor.fetchone()
        except Exception as e:
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            return result
        finally:
            cursor.close()
            connection.close()
