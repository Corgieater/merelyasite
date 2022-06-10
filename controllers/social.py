from flask import *
from models.reviewData import *
from models.userData import *
from controllers.generalFunc import *
import jwt
import math


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
            'movieTitle': item[4],
            'reviewerImgId': item[5]
        }
        review_dic['data']['data'].append(info)
    return review_dic


# 拿頭五篇所有flowing的reviews
def get_latest_five_reviews_from_follows_func():
    try:
        token = request.cookies.get('user_info')
        if token is None:
            return {'error': True}
        data = jwt.decode(token, key, algorithms=["HS256"])

    except Exception as e:
        print('get_latest_five_reviews_from_follows_func from social')
        print(e)
        return None
    else:
        latest_five_reviews = review_database.get_latest_five_reviews_from_follows(data['userId'])
        if len(latest_five_reviews) == 0:
            return {'error': True}
        latest_five_reviews = make_reviews_dic(latest_five_reviews)
        return latest_five_reviews


# 看該使用者有沒有追蹤某個user
def get_is_user_following_func(page_owner):
    try:
        token = request.cookies.get('user_info')
        if token is None:
            return {'error':True}
        data = jwt.decode(token, key, algorithms=["HS256"])

    except Exception as e:
        print('get_is_user_following_func from social')
        print(e)
        return None
    else:
        is_following = user_database.check_is_user_following(data['userId'], page_owner)
        if is_following:
            return {'ok': True}
        else:
            return{'error': True}


# 追蹤別人
def follows_other_people_func(following_name, follower):
    following = user_database.follow_other_user(follower, following_name)
    if following:
        return {'ok': True}
    else:
        return {'error': True,
                'message': 'Something went wrong, please try again'}


# check user review likes
def check_user_review_likes(user_id, review_id):
    is_in_review_like_list = user_database.check_user_state(user_id, review_id, 'reviewLikes')

    if is_in_review_like_list is None:
        is_in_review_like_list = False

    data = {
        'data': {
            'userLikes': is_in_review_like_list,
        }
    }
    return data


# 喜歡這review add review to likes
def add_review_to_likes_func(user_id, review_id):
    if user_id is None:
        return {'error': True,
                'message':'Please log in'}
    reviews_likes_added = user_database.add_to_reviews_likes(user_id, review_id)
    if reviews_likes_added:
        return{'ok': True}
    else:
        return{'error': True,
               'message': 'Something went wrong, please try again'
               }


# delete from reviews users likes
def delete_review_from_likes_func(user_id, review_id):
    if user_id is None:
        return {'error': True,
                'message': 'Please log in'}
    delete_from_reviews_users_likes = user_database.delete_from_reviews_users_likes(user_id, review_id)
    if delete_from_reviews_users_likes:
        return {'ok': True}
    else:
        return {'error': True,
                'message': 'Something went wrong, please try again'
                }


def get_total_review_likes_func(review_id):
    review_likes_count = review_database.get_total_review_likes(review_id)[0]
    data = {'data': {'reviewLikes': review_likes_count}}
    return data


# 拿最近following的朋友喜歡的評論*4
def get_following_latest_like_reviews_func(user_id):
    user_followings_like_reviews = review_database.get_followings_like_reviews(user_id)
    data = {
        'data': {'data': []}
    }
    for review in user_followings_like_reviews:
        info = {
            'reviewId': review[0],
            'movieId': review[1],
            'review': review[2],
            'spoilers': review[3],
            'movieTitle': review[4],
            'reviewer': review[5],
            'reviewerImgId': review[6]
        }
        data['data']['data'].append(info)
    return data


def get_most_popular_reviews_func():
    user_followings_like_reviews = review_database.get_most_popular_reviews()
    data = {
        'data': {'data': []}
    }
    for review in user_followings_like_reviews:
        info = {
            'reviewId': review[0],
            'movieId': review[2],
            'review': review[1],
            'spoilers': review[3],
            'movieTitle': review[4],
            'reviewer': review[5],
            'reviewerImgId': review[7]
        }
        data['data']['data'].append(info)
    return data

