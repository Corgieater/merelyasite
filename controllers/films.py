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


# # 更新或加入評分
# def rating_func(rate, user_id, film_id):
#     if user_id is None:
#         return {
#             'error': True,
#             'message': 'Please log in'
#         }
#     result = review_database.rating(rate, user_id, film_id)
#     if result is True:
#         return {'ok': True}
#
#     else:
#         return{
#             'error': 'Something went wrong, please try again'
#         }
#
#
# # 拿上次評分
# def get_rate_func(user_id, movie_id):
#     rate = review_database.get_rate_data(user_id, movie_id)
#     if rate:
#         data = {
#             'data': {'rate': rate}
#         }
#         return data
#     else:
#         return {
#             'data': {'rate': None}
#         }
#
#
# # 刪除評分
# def delete_rate_func(film_id, user_id):
#     data_deleted = review_database.delete_rate_data(film_id, user_id)
#     if data_deleted:
#         return {
#             'ok': True
#         }
#     else:
#         return{
#             'error': False,
#             'message': 'Deleting failed, please try again'
#         }
#
#
# # 拿均分
# def get_average_rate_func(film_id):
#     data = review_database.get_average_rate_data(film_id)
#
#     if data:
#         return {
#             'data': {'totalCount': data[0],'average':data[1]}
#         }
#     else:
#         return {
#             'error': False
#         }
#
#
# # 評論相關
# # 留評論
# def film_review_func(movie_review, film_id, current_date, watched_date, user_id, spoilers,
#                      review_id=None, from_where=None):
#     if from_where == 'userProfileReviewAgain':
#         movie_and_user_id = review_database.get_movie_id_and_user_id_for_review_again(review_id)
#         film_id = movie_and_user_id[0]
#         user_id = movie_and_user_id[1]
#         if user_id is None and from_where is None:
#             return {
#                 'error': True,
#                 'message': 'Please log in'
#             }
#         result = review_database.write_review(movie_review, film_id, current_date, watched_date, user_id, spoilers)
#     else:
#         result = review_database.write_review(movie_review, film_id, current_date, watched_date, user_id, spoilers)
#
#     if result is True:
#         return {
#             'ok': True
#         }
#     else:
#         return {
#             'error': False,
#             'message': 'Review failed, please try again'
#         }
#
#
# # for index
# def get_latest_reviews_func():
#     latest_reviews = review_database.get_latest_reviews_for_index()
#     total_reviews = review_database.get_all_reviews_count()
#     data = {
#         'data': {'data': [],'totalReviews': total_reviews[0]}
#     }
#     for reviews in latest_reviews:
#         info = {
#             'userName': reviews[0],
#             'reviewMovie': reviews[1],
#             'reviewId': reviews[2],
#             'reviewMovieId': reviews[3],
#
#         }
#         data['data']['data'].append(info)
#
#     return data


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

