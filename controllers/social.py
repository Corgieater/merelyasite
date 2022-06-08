from flask import *
from models.reviewData import *
from models.userData import *
import jwt
import os
import math
import requests
from os.path import basename
import boto3

review_database = ReviewDatabase()
user_database = UserDatabase()
key = os.getenv('JWT_SECRET_KEY')

key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')

client = boto3.client('s3',
                      aws_access_key_id=key_id,
                      aws_secret_access_key=secret_key
                      )


def up_load_to_s3(img, user_id):
    # 丟S3
    client.put_object(
        Bucket=bucket_name,
        Body=img,
        Key=f'userPic/userProfileImg-{user_id}.jpg',
        ContentType='image/jpeg',
    )

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


# 拿頭五篇所有flowing的reviews
def get_latest_five_reviews_from_follows_func():
    try:
        token = request.cookies.get('user_info')
        if token is None:
            return {'error': True}
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

# watchlist
# check watchlist
def get_watchlist_by_page_func(page_master, page):
    movies_in_watchlist = user_database.get_total_movie_in_watchlist_by_name(page_master)[0]
    total_page = math.ceil(movies_in_watchlist/24)
    if page is None:
        page = 1
    page = int(page)-1
    watchlist = user_database.get_watchlist(page_master, page)
    data = {
        'data': {
            'data': [],
            'totalMovies':movies_in_watchlist
        }
    }
    print('wathvspigj-------\n',watchlist)
    for movie in watchlist:
        data['data']['data'].append(movie)
    data = make_page(data, 1, total_page)
    print(data)
    return data

# check user movie state movielist/likes
def check_user_movie_state_func(user_id, movie_id):
    print(user_id, movie_id,'checking')
    is_in_watchlist = user_database.check_user_state(user_id, movie_id, 'watchlist')
    is_in_movie_likes_list = user_database.check_user_state(user_id, movie_id, 'movieLikes')
    print('oyoyyo user state here',is_in_watchlist, is_in_movie_likes_list)
    if is_in_watchlist is None:
        is_in_watchlist = False
    if is_in_movie_likes_list is None:
        is_in_movie_likes_list = False
    print('oyoyyo user state here', is_in_watchlist, is_in_movie_likes_list)
    data = {
        'data': {
            'userWatchlist': is_in_watchlist,
            'userLikes': is_in_movie_likes_list
        }
    }
    return data


# check user review likes
def check_user_review_likes(user_id, review_id):
    is_in_review_like_list = user_database.check_user_state(user_id, review_id, 'reviewLikes')
    print('6666 user review state here', is_in_review_like_list)
    if is_in_review_like_list is None:
        is_in_review_like_list = False
    print('6666 user review state here', is_in_review_like_list)
    data = {
        'data': {
            'userLikes': is_in_review_like_list,
        }
    }
    return data


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


def add_movie_to_likes_func(user_id, movie_id):
    if user_id is None:
        return {'error': True,
                'message':'Please log in'}
    movies_likes_added = user_database.add_to_movies_likes(user_id, movie_id)
    if movies_likes_added:
        return{'ok': True}
    else:
        return{'error': True,
               'message': 'Something went wrong, please try again'
               }


# delete from movies users likes
def delete_movie_from_likes_func(user_id, movie_id):
    if user_id is None:
        return {'error': True,
                'message':'Please log in'}
    delete_from_movies_users_likes = user_database.delete_from_movies_users_likes(user_id, movie_id)
    if delete_from_movies_users_likes:
        return {'ok': True}
    else:
        return {'error': True,
                'message': 'Something went wrong, please try again'
                }

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
    print('review_likes_count',review_likes_count)
    data = {'data':{'reviewLikes': review_likes_count}}
    return data


# 拿最近following的朋友喜歡的評論*4
def get_following_latest_like_reviews_func(user_id):
    user_followings_like_reviews = review_database.get_followings_like_reviews(user_id)
    print(user_followings_like_reviews)
    data = {
        'data':{'data':[]}
    }
    for review in user_followings_like_reviews:
        info = {
            'reviewId': review[0],
            'movieId': review[1],
            'review': review[2],
            'spoilers': review[3],
            'movieTitle': review[4],
            'reviewer': review[5]
        }
        data['data']['data'].append(info)
    print(user_followings_like_reviews)
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
            'reviewer': review[5]
        }
        data['data']['data'].append(info)
    print(user_followings_like_reviews)
    return data


# 上傳user profile 照片
def upload_user_profile_pic_func(user_id, img):
    img_name = f'userProfileImg-{user_id}'
    try:
        up_load_to_s3(img, user_id)
    except Exception as e:
        print('we got problem on user pic upload to s3')
        print(e)
    pic_uploaded = user_database.add_user_profile_pic(user_id, img_name)
    if pic_uploaded:
        return {
            'ok': True
        }
    else:
        return {
            'error':True,
            'message': 'Something went wrong, please try again'
        }


def get_user_profile_pic_func(user_id):
    user_profile_pic_name = user_database.get_user_profile_pic(user_id)
    print(user_profile_pic_name, 'user_profile_pic_name from social')
    if user_profile_pic_name is not None:
        return {
            'data': {
                'picName': user_profile_pic_name[0]
            }
        }
    else:
        return {
            'data': None
        }

