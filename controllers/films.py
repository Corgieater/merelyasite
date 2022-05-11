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
        'plot': film_data[6],
        'average':film_data[7],
    }

    return dic


def get_film_by_id_func(film_id):
    data = movie_database.get_film_by_id(film_id)
    if data is None:
        return {
            'error': True,
            'message': 'There is no such id, please check it again'
        }
    data_dic = make_dic(data)
    return data_dic


def write_review_func():
    pass


def renew_rate_func(rate, user_id, movie_id):
    # data = (rate, user_id, movie_id)
    rate_updated = review_database.rating(rate, user_id, movie_id)
    if rate_updated:
        return {'ok': True}
    else:
        return{
            'error':'Something went wrong, please try again'
        }


def get_rate_func(user_id, movie_id):
    pass