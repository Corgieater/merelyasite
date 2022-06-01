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


# 拿頭五篇所有flowing的reviews
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
        print(data)

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


# check watchlist
def check_movie_in_watchlist_func(user_id, movie_id):
    movie_is_in_watchlist = user_database.check_watchlist(user_id, movie_id)
    if movie_is_in_watchlist is not None:
        return{'ok': True}
    else:
        return{'none': True}

# 加入待看清單 watchlist
def add_movie_to_watchlist_func(user_id, movie_id):
    if user_id is None:
        return {'error': True,
                'message':'Please log in'}
    add_to_watchlist = user_database.add_to_watchlist(user_id, movie_id)
    if add_to_watchlist:
        return{'ok': True}
    else:
        return{'error': True,
               'message': 'Something went wrong, please try again'
               }

# delete from watchlist
def delete_movie_from_watchlist_func(user_id, movie_id):
    if user_id is None:
        return {'error': True,
                'message':'Please log in'}
    delete_from_watchlist = user_database.delete_from_watchlist(user_id, movie_id)
    if delete_from_watchlist:
        return {'ok': True}
    else:
        return {'error': True,
                'message': 'Something went wrong, please try again'
                }