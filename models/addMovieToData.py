import mysql.connector
from mysql.connector import pooling
import json
import os
from dotenv import load_dotenv
from models.databaseClass import pool as p
from models.movieData import *
import random
import time

# load_dotenv()
#
#
# MYSQL_HOST = os.getenv('MYSQL_HOST')
# MYSQL_USER = os.getenv('MYSQL_USER')
# MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
# MYSQL_DATABASE = 'movie'

def random_delay(time_list):
    delay_choices = time_list
    delay = random.choice(delay_choices)
    time.sleep(delay)

class ImportDatabase:
    def add_to_database(self, movie_info, directors, actors, genres):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            print('---add to database callllllll------\n')
            print(movie_info)
            cursor.execute('INSERT INTO movies_info(movie_id, title, year, story_line, tagline)'
                           ' VALUES(DEFAULT,%s,%s,%s,%s)',
                           (movie_info[0], movie_info[1], movie_info[2],movie_info[3]))
            cursor.execute('SELECT LAST_INSERT_ID()')

            last_insert_movie_id = cursor.fetchone()[0]
            print('last insert', last_insert_movie_id)

            # for director in directors:
            #     print('start director', director)
            #     director_id = self.find_input_from_table('director_id', 'directors', 'name', director)
            #     random_delay([2])
            #     if director_id is not None:
            #         print(f'{director_id} {director} is exist')
            #         self.add_relationship((director_id, last_insert_movie_id),'director')
            #     else:
            #         print(f'{director} not in database')
            #         new_director_id = self.add_subject_to_database_by_type(director, 'director')
            #         print('new director added',new_director_id)
            #         self.add_relationship((new_director_id, last_insert_movie_id), 'director')
            #
            # for actor in actors:
            #     print('start actor', actor)
            #     actor_id = self.find_input_from_table('actor_id', 'actors', 'name', actor)
            #     random_delay([2])
            #     if actor_id is not None:
            #         self.add_relationship((actor_id, last_insert_movie_id), 'actor')
            #     else:
            #         new_actor_id = self.add_subject_to_database_by_type(actor, 'actor')
            #         print('new actor added', new_actor_id)
            #         self.add_relationship((new_actor_id, last_insert_movie_id), 'actor')
            #
            # for genre in genres:
            #     print('start genre', genre)
            #     genre_id = self.find_input_from_table('genre_id', 'genres', 'type', genre)
            #     random_delay([2])
            #     if genre_id is not None:
            #         self.add_relationship((genre_id, last_insert_movie_id), 'genre')
            #     else:
            #         new_genre_id = self.add_subject_to_database_by_type(genre, 'genre')
            #         print('new genre added', new_genre_id)
            #         self.add_relationship((new_genre_id, last_insert_movie_id), 'genre')

        except Exception as e:
            print('add_to_database',)
            print(e)
            connection.rollback()
            return False
        else:
            connection.commit()
            return last_insert_movie_id
        finally:
            cursor.close()
            connection.close()

    def find_in_database(self, title, year):
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

    def check_last_movie_id(self):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute('SELECT id FROM movie_info ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            print('result in check_last_movie_id-----\n', result)
            if result is None:
                return None
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
        print(input_tuple)
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
            print(f'searching SELECT {id_type} FROM {table} WHERE {column} = %s', (input_content,))
            cursor.execute(f'SELECT {id_type} FROM {table} WHERE {column} = %s', (input_content,))
            input_id = cursor.fetchone()
            print(f'trying finding {input_content} in table ',input_id)
            if input_id is not None:
                print(input_id)
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


    # 多功能添加 好像可以改簡單點啦... 1 line or so
    def add_subject_to_database_by_type(self, subject, input_type):
        connection = p.get_connection()
        cursor = connection.cursor()
        try:
            if input_type == 'director':
                print(subject)
                cursor.execute('INSERT INTO directors(director_id, name) '
                               'VALUES(DEFAULT,%s)', (subject,))
            if input_type == 'actor':
                print(subject)
                cursor.execute('INSERT INTO actors(actor_id, name) '
                               'VALUES(DEFAULT,%s)', (subject,))
            if input_type == 'genre':
                print(subject)
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
