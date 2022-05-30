from flask import *
from models.reviewData import *
from models.userData import *
import jwt
import os

review_database = ReviewDatabase()
user_database = UserDatabase()
key = os.getenv('JWT_SECRET_KEY')


def make_reviews_dic(data):
    review_dic = {
        'data': {
            'data': []
        }
    }
    for item in data:
        info = {
            'followUserName': item[0],
            'reviewId': item[1],
            'movieId': item[2],
            'reviewDate': item[3],
            'movieTitle': item[4]
        }
        review_dic['data']['data'].append(info)
    return review_dic



# 拿頭五篇所有追蹤者的reviews
def get_latest_five_reviews_from_follows_func():
    try:
        token = request.cookies.get('user_info')
        if token is None:
            return
        data = jwt.decode(token, key, algorithms=["HS256"])
        print(data)

    except Exception as e:
        print('get_latest_five_reviews_from_follows_func from social')
        print(e)
        return None
    else:
        latest_five_reviews = review_database.get_latest_five_reviews_from_follows(data['userId'])
        if len(latest_five_reviews) is 0:
            return None
        latest_five_reviews = make_reviews_dic(latest_five_reviews)
        return latest_five_reviews


# 追蹤別人
def follows_other_people_func():
    try:
        token = request.cookies.get('user_info')
        if token is None:
            return {
                'data': None
            }
        data = jwt.decode(token, key, algorithms=["HS256"])

    except Exception as e:
        print(e)
        return {
            'data': None
        }
    else:
        return follow_other_user(data['userId'])