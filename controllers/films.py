from models.movieData import *
from models.reviewData import *
import os

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

# 用ID拿電影
def get_film_by_id_func(film_id):
    data = movie_database.get_film_by_id(film_id)
    if data is None:
        return {
            'error': True,
            'message': 'There is no such id, please check it again'
        }
    return data


# 用導演拿電影
def get_films_by_director_func(director):
    data = movie_database.get_film_by_director(director)
    print(data)
    if data is None:
        return {
            'error': True,
            'message': 'There is no such person, please check it again'
        }

    return data


# 用genre/演員拿電影(因為太多所以要頁數)
def get_films_by_input_func(ser_input, input_type, start_index=0):
    data = movie_database.get_film_by_input(ser_input, input_type, start_index)
    print(data)
    if data is None:
        return {
            'error': True,
            'message': 'There is no such person, please check it again'
        }
    data_dic = {'data': {
        'id_list': [],
    }}
    for film_id in data:
        data_dic['data']['id_list'].append(film_id[0])
    return data_dic


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