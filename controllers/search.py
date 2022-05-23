from models.movieData import *
import os
import math

key = os.getenv('JWT_SECRET_KEY')

database = MovieDatabase()


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

    print('serachdata', searched_data)
    return searched_data


def get_info_func(user_input, page):
    data_count = database.get_total_data_count(user_input)[0]
    print('data count', data_count)
    if data_count is None:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
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
    # if len(dic_data['data']) == 0:
    #     return {
    #         'error': True,
    #         'message': 'No such key word, please try another'
    #     }
    return dic_data

