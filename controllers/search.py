from models.movieData import *
from flask import *
import jwt
import os
from datetime import timedelta

key = os.getenv('JWT_SECRET_KEY')

# 名稱要改嗎? 畢竟到時候要一起搜review?
database = MovieDatabase()


def make_dic(info):
    searched_data = {'data': []}

    for info_data in info:
        dic = {
            'id': info_data[0],
            'title': info_data[1],
            'year': info_data[2],
            'rating': info_data[3],
            'directors': info_data[4].split(','),
            'stars': info_data[5].split(','),
            'genre': info_data[6].split(','),
            'plot': info_data[7]
        }
        searched_data['data'].append(dic)

    return searched_data


# def get_info_func(user_input):
#     info = database.get_info(user_input)
#     dic_data = make_dic(info)
#     if len(dic_data) == 0:
#         return {
#             'error': True,
#             'message': 'No such key word, please try another'
#         }
#     encoded_data = jwt.encode(dic_data, key, algorithm="HS256")
#     res = make_response({'ok': True})
#     res.set_cookie('user_search', encoded_data, timedelta(days=7))
#     return res

# test
def get_info_func(user_input):
    info = database.get_info(user_input)
    dic_data = make_dic(info)
    if len(dic_data) == 0:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
    return dic_data


def check_cookie_func():
    encoded_cookie = request.cookies.get('user_search')
    # 防範不知道怎樣會發生的沒cookie事件
    if encoded_cookie is None:
        return {
            'data': None
        }
    searched_cookie = jwt.decode(encoded_cookie, key, algorithms=['HS256'])
    print(searched_cookie)

    return searched_cookie
