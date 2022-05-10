from models.movieData import *
import os

key = os.getenv('JWT_SECRET_KEY')

database = MovieDatabase()

def make_dic(film_data):
    print(film_data)
    dic = {
        'id':film_data[0],
        'title':film_data[1],
        'year': film_data[2],
        'rating': film_data[3],
        'directors': film_data[4].split(','),
        'stars': film_data[5].split(','),
        'genres': film_data[6].split(','),
        'plot': film_data[7]
    }

    return dic


def get_film_by_id_func(film_id):
    data = database.get_film_by_id(film_id)
    data_dic = make_dic(data)
    return data_dic
