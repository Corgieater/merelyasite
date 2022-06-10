from models.movieData import *
from models.userData import *
from models.reviewData import *
from controllers.generalFunc import *
import os
import math

key = os.getenv('JWT_SECRET_KEY')

movie_database = MovieDatabase()
user_database = UserDatabase()
review_database = ReviewDatabase()


# # films controller也有
# def make_page(data, page, total_page):
#     data['currentPage'] = page+1
#     data['nextPage'] = None
#     data['totalPages'] = total_page
#
#     if page < total_page:
#         data['nextPage'] = page + 1
#     else:
#         data['nextPage'] = None
#     return data


def make_dic(info, page, total_page):
    page = int(page)+1
    searched_data = {'data': [], 'currentPage': page, 'nextPage': None, 'totalPages': total_page}
    if page < total_page:
        searched_data['nextPage'] = page+1
    else:
        searched_data['nextPage'] = None
    for info_data in info:
        dic = {
            'id': info_data[0],
            'title': info_data[1],
            'year': info_data[2],
            'directors': info_data[3].split(',')
        }
        searched_data['data'].append(dic)

    return searched_data


def make_user_dic(data, followed_info, following_info, page, total_page):
    data_dic = {
        'data': {
            'data': []
        }
    }
    page = int(page) + 1
    if page < total_page:
        data_dic['nextPage'] = page + 1
    else:
        data_dic['nextPage'] = None

    # followed_info, following_info
    for i in range(len(data)):
        info_dic = {
            'userName': data[i][0],
            'userImageId':data[i][1],
            'followingNum': following_info[i][0],
            'followerNum': followed_info[i][0]
        }
        data_dic['data']['data'].append(info_dic)
    return data_dic


def make_reviews_search_dic(data):
    review_dic = {'data': {
        'data': []
    }
    }
    for info in data:
        dic = {
            'movieId': info[0],
            'movieTitle': info[1],
            'year': info[2],
            'reviewId': info[3],
            'review': info[4],
            'spoilers': info[5],
            'reviewUserImgId': info[6],
            'reviewUserName': info[7]
        }
        review_dic['data']['data'].append(dic)
    return review_dic


# 拿電影資料 搜尋用
def get_movie_info_func(user_input, page):
    data_count = movie_database.get_total_data_count_from_type(user_input, 'movie')[0]
    if data_count is 0:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
    total_page = math.ceil(data_count / 20)
    if page is None:
        page = 1
    page = int(page)-1
    info = movie_database.get_movie_info_by_keyword(user_input, page)

    if info is False:
        return {
            'error': True
        }
    dic_data = make_dic(info, page, total_page)

    return dic_data


def get_data_by_type_func(query, page, data_type):
    data_count = 0
    if page is None:
        page = 1
    page = int(page) - 1
    if data_type == 'director':
        data_count = movie_database.get_total_data_count_from_type(query, 'director')

    if data_type == 'actor':
        data_count = movie_database.get_total_data_count_from_type(query, 'actor')

    if data_count is False or data_count[0] is 0:
        return {
            'error': True,
            'message': 'There is no such keyword, please check it again'
        }

    total_page = math.ceil(data_count[0] / 20)

    info = None
    if data_type == 'director':
        info = movie_database.get_director_by_name(query, page, data_count[0])

    if data_type == 'actor':
        info = movie_database.get_actor_by_name(query, page, data_count[0])
    info = make_page(info, page, total_page)
    return info


# GENRE拿電影
def get_films_by_genre_func(genre, page):
    data_count = movie_database.get_total_data_count_from_type(genre, 'genre')[0]
    if data_count is 0:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
    total_page = math.ceil(data_count / 20)
    if page is None:
        page = 1
    page = int(page)-1
    info = movie_database.get_film_by_genre(genre, page)

    if info is False:
        return {
            'error': True
        }
    dic_data = make_dic(info, page, total_page)

    return dic_data


# user name get users HERE
def get_users_by_name_func(name, page):
    data_count = user_database.get_total_user_count_by_name(name)[0]
    if data_count is 0:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
    total_page = math.ceil(data_count / 20)
    if page is None:
        page = 1
    page = int(page)-1
    info = user_database.get_users_by_name(name, page)
    followed_info = user_database.get_user_followed_count(name, page)
    following_info = user_database.get_user_following_count(name, page)

    if info is False:
        return {
            'error': True
        }
    dic_data = make_user_dic(info, followed_info, following_info,page, total_page)

    return dic_data


def get_reviews_from_title_or_content_func(review_query, page):
    data_count = review_database.get_total_review_count_by_title_and_content(review_query)[0]
    if data_count == 0:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
    total_page = math.ceil(data_count / 20)
    if page is None:
        page = 1
    page = int(page) - 1
    info = review_database.get_review_by_title_and_content(review_query, page)

    if info is False or len(info) == 0:
        return {
            'error': True
        }

    dic_data = make_reviews_search_dic(info)
    make_page(dic_data, page, total_page)

    return dic_data
