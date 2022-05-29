from models.movieData import *
import os
import math

key = os.getenv('JWT_SECRET_KEY')

database = MovieDatabase()


# films controller也有
def make_page(data, page, total_page):
    print(data, page, total_page)
    data['currentPage'] = page
    data['nextPage'] = None
    data['totalPages'] = total_page

    if page < total_page:
        data['nextPage'] = page + 1
    else:
        data['nextPage'] = None
    return data


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


# 目前只能找電影 看之後可不可以改成找全部 no:(
def get_info_func(user_input, page):
    print(user_input, 'userInput')
    data_count = database.get_total_data_count_from_type(user_input, 'movie')[0]
    if data_count is 0:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
    print('data_count', data_count)
    total_page = math.ceil(data_count / 20)
    print(total_page)
    if page is None:
        page = 1
    page = int(page)-1
    info = database.get_info(user_input, page)
    print(info, 'info')

    if info is False:
        return {
            'error': True
        }
    dic_data = make_dic(info, page, total_page)

    return dic_data

# 拿演員導演資料 films/controller也有一個
def get_data_by_type_func(query, page, data_type):
    data_count = 0
    if page is None:
        page = 1
    page = int(page) - 1
    if data_type == 'director':
        data_count = database.get_total_data_count_from_type(query, 'director')
        print(data_count, 'director')

    if data_type == 'actor':
        data_count = database.get_total_data_count_from_type(query, 'actor')
        print(data_count, 'actor')

    if data_count is False or data_count[0] is 0:
        return {
            'error': True,
            'message': 'There is no such keyword, please check it again'
        }

    total_page = math.ceil(data_count[0] / 20)

    info = None
    if data_type == 'director':
        info = database.get_director_by_name(query, page)
        print()
    if data_type == 'actor':
        info = database.get_actor_by_name(query, page)
    info = make_page(info, page, total_page)
    print(info)
    return info


# GENRE拿電影 HERE
def get_films_by_genre_func(genre, page):
    print(genre, 'userInput')
    data_count = database.get_total_data_count_from_type(genre, 'genre')[0]
    if data_count is 0:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
    print('data_count', data_count)
    total_page = math.ceil(data_count / 20)
    print(total_page)
    if page is None:
        page = 1
    page = int(page)-1
    info = database.get_film_by_genre(genre, page)
    print(info, 'info')

    if info is False:
        return {
            'error': True
        }
    dic_data = make_dic(info, page, total_page)

    return dic_data
