from models.movieData import *
from models.reviewData import *
import os

key = os.getenv('JWT_SECRET_KEY')

movie_database = MovieDatabase()
review_database = ReviewDatabase()


def make_review_dic(data):
    data_dic = {
        'data': []
    }

    for info in data:
        print(data)
        dic = {
            'review': info[0],
            'reviewDay': info[1],
            'watchedDay': info[2],
            'reviewId': info[3],
            'spoilers': info[4],
            'filmId': info[5],
            'filmTitle': info[6],
            'filmYear': info[7],
            'userRate': info[8]
        }
        data_dic['data'].append(dic)
    return data_dic


def get_user_latest_five_reviews_func(user_name):
    data = review_database.get_reviews_data(user_name)
    print(data)
    data_dic = make_review_dic(data)
    print(data_dic)
    return data_dic
