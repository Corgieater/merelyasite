from models.movieData import *
from models.reviewData import *
import os
import math

key = os.getenv('JWT_SECRET_KEY')

movie_database = MovieDatabase()
review_database = ReviewDatabase()

def make_review_dic(data):
    data_dic = {
        'data': []
    }

    for info in data:
        print(info, 'from controller user profile')
        dic = {
            'review': info[4],
            'reviewDay': info[5],
            'watchedDay': info[6],
            'spoilers': info[7],
            'filmId': info[3],
            'filmTitle': info[0],
            'filmYear': info[1],
            'userRate': info[8],
            'reviewId': info[2]
        }
        data_dic['data'].append(dic)
    return data_dic


def make_page(data, page, total_page):
    page = int(page)
    data['currentPage'] = page
    data['nextPage'] = None
    data['totalPages'] = total_page

    if page < total_page:
        data['nextPage'] = page + 1
    else:
        data['nextPage'] = None
    return data


def get_user_profile_review_each_func(review_id):
    data = review_database.get_review_by_review_id(review_id)[0]
    print('get_user_profile_review_each_func',data)
    if data is None:
        return {'error':True,
                'message':'Something is wrong, please try again'
                }
    make_data_dic = {
        'data':{
            'movieId': data[1],
            'movieReview': data[2],
            'reviewDate': data[3],
            'watchedDate': data[4],
            'spoiler': data[5],
            'movieTitle': data[6],
            'movieYear': data[7],
            'movieRate': data[8]
        }
    }
    return make_data_dic


# get lasted reviews by 5
def get_user_latest_five_reviews_func(user_name):
    data = review_database.get_reviews_data(user_name)
    data_dic = make_review_dic(data)
    return data_dic

# get all reviews
def get_reviews_by_page_func(user_name, page):
    data = review_database.get_user_reviews_count(user_name)
    review_counts = data[0]
    data = review_database.get_reviews_data(user_name, page)
    total_page = math.ceil(review_counts/20)
    data_dic = make_review_dic(data)
    make_page(data_dic, page, total_page)
    return data_dic


# update user review
def update_user_profile_review_func(review_id, movie_review, watched_date, spoilers):
    review_updated = review_database.update_review(review_id, movie_review, watched_date, spoilers)
    if review_updated:
        return {
            'ok':True,
        }
    else:
        return{
            'error':True,
            'message': 'Something goes wrong, please try again'
        }


# delete user review
def delete_user_profile_review_func(review_id):
    review_deleted = review_database.delete_review(review_id)
    if review_deleted:
        return {
            'ok': True
        }
    else:
        return {
            'error': False,
            'message': 'Review deleting failed, please try again'
        }
