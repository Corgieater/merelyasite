from models.movieData import *
from models.reviewData import *
import os
import math

key = os.getenv('JWT_SECRET_KEY')

movie_database = MovieDatabase()
review_database = ReviewDatabase()



def make_dic(film_data):
    print(film_data)
    dic = {
        'id':film_data[0],
        'title':film_data[1],
        'year': film_data[2],
        'directors': film_data[3].split(','),
        'stars': film_data[4].split(','),
        'genres': film_data[5].split(','),
        'plot': film_data[6]
    }

    return dic


def make_page(data, page, total_page):
    page = int(page) + 1
    data['data']['currentPage'] = page
    data['data']['nextPage'] = None
    data['data']['totalPages'] = total_page

    if page < total_page:
        data['nextPage'] = page + 1
    else:
        data['nextPage'] = None

    return data

# 用ID拿電影
def get_film_by_id_func(film_id):
    data = movie_database.get_film_by_id(film_id)
    if data is None:
        return {
            'error': True,
            'message': 'There is no such id, please check it again'
        }
    return data


# 用導演拿電影 OK
def get_films_by_director_func(director):
    data = movie_database.get_film_by_director(director)
    print(data)
    if data is None:
        return {
            'error': True,
            'message': 'There is no such person, please check it again'
        }

    return data


# 演員拿電影 OK
def get_films_by_actor_func(actor, page):
    data_count = movie_database.get_total_data_count_from_type(actor, 'actor')[0]
    if data_count is None:
        return {
            'error': True,
            'message': 'There is no such person, please check it again'
        }
    total_page = math.ceil(data_count / 20)
    if page is None:
        page = 1
    page = int(page) - 1
    info = movie_database.get_film_by_actor(actor, page)
    info = make_page(info, page, total_page)
    return info
    # data = movie_database.get_film_by_actor(actor, start_index)
    # data_dic = {'data': {
    #     'movieId': [],
    # }}
    # for film_id in data:
    #     data_dic['data']['movieId'].append(film_id[2])
    # return data_dic


# 更新或加入評分
def renew_rate_func(rate, user_id, film_id):
    if user_id is None:
        print('NOPELPELE')
    print('renew_rate_func', rate, user_id, film_id)
    rate_updated = review_database.rating(rate, user_id, film_id)
    if rate_updated:
        return {'ok': True}
    else:
        return{
            'error':'Something went wrong, please try again'
        }


# 拿上次評分
def get_rate_func(user_id, movie_id):
    rate = review_database.get_rate_data(user_id, movie_id)
    if rate:
        data = {
            'data': {'rate': rate[0]}
        }
        return data
    else:
        return {
            'data': {'rate':None}
        }

# 刪除評分
def delete_rate_func(film_id, user_id):
    print(film_id, user_id)
    data_deleted = review_database.delete_rate_data(film_id, user_id)
    if data_deleted:
        return {
            'ok': True
        }
    else:
        return{
            'error': False,
            'message': 'Deleting failed, please try again'
        }


# 拿均分
def get_average_rate_func(film_id):
    data = review_database.get_average_rate_data(film_id)
    print('print data',data)
    if data:
        return {
            'data': {'totalCount': data[0],'average':data[1]}
        }
    else:
        return {
            'error': False
        }


# 評論相關
# 留評論
def film_review_func(user_review, film_id, current_date, watched_date, user_id):
    review_added = review_database.write_review(user_review, film_id, current_date, watched_date, user_id)
    if review_added:
        return {
            'ok': True
        }
    else:
        return {
            'error': False,
            'message': 'Review failed, please try again'
        }


# 刪除評論
def film_delete_func(film_id, user_id):
    review_deleted = review_database.delete_review(film_id, user_id)
    if review_deleted:
        return {
            'ok': True
        }
    else:
        return {
            'error': False,
            'message': 'Review deleting failed, please try again'
        }

# 改評論
def film_edit_func(user_review, film_id, current_date, watched_date, user_id):
    review_edited = review_database.edit_review(user_review, film_id, current_date, watched_date, user_id)
    if review_edited:
        return {
            'ok': True
        }
    else:
        return {
            'error': False,
            'message': 'Review failed, please try again'
        }


# 拿評論
def get_reviews_func(user_name):
    data = review_database.get_reviews_data(user_name)
    print(data)
    if data:
        return {
            'data': data
        }
    else:
        return {
            'error': False
        }