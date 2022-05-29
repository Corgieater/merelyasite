from flask import *
from models.reviewData import *
import jwt
import os

database = ReviewDatabase()
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

def get_latest_five_reviews_from_follows_func():
    try:
        token = request.cookies.get('user_info')
        if token is None:
            return {
                'data': None
            }
        data = jwt.decode(token, key, algorithms=["HS256"])
        print(data)
        if data:
            latest_five_reviews = database.get_latest_five_reviews_from_follows(data['userId'])
            if len(latest_five_reviews) is 0:
                return
            latest_five_reviews = make_reviews_dic(latest_five_reviews)
            print(latest_five_reviews)
            return latest_five_reviews

    except Exception as e:
        print(e)
        return {
            'data': None
        }

