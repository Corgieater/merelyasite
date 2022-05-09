from models.movieData import *

# 名稱要改嗎? 畢竟到時候要一起搜review?
data = MovieDatabase()


def make_json(info):
    json = {'data': []}

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
        json['data'].append(dic)
    return json


def get_info_func(user_input):
    info = data.get_info(user_input)
    json = make_json(info)
    return json


