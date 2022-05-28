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
            'review': info[5],
            'reviewDay': info[6],
            'watchedDay': info[7],
            'spoilers': info[8],
            'filmId': info[4],
            'filmTitle': info[1],
            'filmYear': info[2],
            'userRate': info[9],
            'reviewId': info[0]
        }
        data_dic['data'].append(dic)
    return data_dic


def make_page(data, page, total_page):
    page = int(page)
    print('makepage-----',data, page)
    print('the type of ', page, type(page))
    data['currentPage'] = page
    data['nextPage'] = None
    data['totalPages'] = total_page

    if page < total_page:
        data['nextPage'] = page + 1
    else:
        data['nextPage'] = None
    return data


# 評分另外拿 get latest 5 reviews
def get_user_latest_five_reviews_func(user_name):
    data = review_database.get_reviews_data(user_name)
    data_dic = make_review_dic(data)
    return data_dic

# 另外拿太浪費資源 要怎辦呢~"~
# 評分另外拿 get all reviews
def get_reviews_by_page_func(user_name, page):
    print('page = ', page)
    data = review_database.get_user_reviews_count_and_user_id(user_name)
    review_counts = data[0]
    user_id = data[1]
    print('from get review by page func ', review_counts, user_id)
    data = review_database.get_reviews_data(user_name, page)
    print('get_reviews_by_page_func', data)
    total_page = math.ceil(review_counts/20)
    data_dic = make_review_dic(data)
    print('page = ', page)
    make_page(data_dic, page, total_page)
    return data_dic

