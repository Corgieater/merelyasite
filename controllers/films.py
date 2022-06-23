from models.movieData import *
from models.userData import *
from controllers.generalFunc import *
import os
import math

key = os.getenv('JWT_SECRET_KEY')

movie_database = MovieDatabase()
user_database = UserDatabase()


def get_data_by_type_func(query, page, data_type):
    data_count = 0
    if page is None:
        page = 1
    page = int(page) - 1
    if data_type == 'director':
        data_count = movie_database.get_total_data_count_from_type(query, 'director')

    if data_type == 'actor':
        data_count = movie_database.get_total_data_count_from_type(query, 'actor')

    if data_count is False or data_count[0] == 0:
        return {
            'error': True,
            'message': 'There is no such keyword, please check it again'
        }

    total_page = math.ceil(data_count[0] / 20)

    info = None
    if data_type == 'director':
        info = movie_database.get_director_by_name(query, page)
    if data_type == 'actor':
        info = movie_database.get_actor_by_name(query, page)
    info = make_page(info, page, total_page)
    return info


# 用ID拿電影
def get_movie_by_id_func(film_id):
    data = movie_database.get_film_by_id(film_id)
    if data is None:
        return {
            'error': True,
            'message': 'There is no such id, please check it again'
        }
    return data


# 用導演拿電影
def get_movies_by_director_func(director, page):
    data_count = movie_database.get_total_data_count_from_type(director, 'director_movies')

    if data_count == 0:
        return {
            'error': True,
            'message': 'There is no such person, please check it again'
        }
    total_page = math.ceil(data_count[0] / 20)
    if page is None:
        page = 1
    page = int(page) - 1
    info = movie_database.get_film_by_director(director, page)
    if info is False:
        return {
            'error': True,
            'message': 'Wrong keyword, please try again'
        }
    info = make_page(info, page, total_page)

    return info


# 演員拿電影
def get_movies_by_actor_func(actor, page):
    data_count = movie_database.get_total_data_count_from_type(actor, 'actor')

    if data_count == 0:
        return {
            'error': True,
            'message': 'There is no such person, please check it again'
        }
    total_page = math.ceil(data_count[0] / 20)
    if page is None:
        page = 1
    page = int(page) - 1
    info = movie_database.get_film_by_actor(actor, page)
    if info is False:
        return {
            'error': True,
            'message': 'Wrong keyword, please try again'
        }
    info = make_page(info, page, total_page)
    return info


# 拿本周最多like的電影
def get_most_popular_movies_this_week_func():
    most_popular_movies = movie_database.get_most_popular_movies_for_index()
    data = {
        'data': {'data': []}
    }
    for reviews in most_popular_movies:
        info = {
            'movieId': reviews[0],
            'totalLikes': reviews[1],
        }
        data['data']['data'].append(info)

    return data

