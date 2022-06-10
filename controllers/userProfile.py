from models.movieData import *
from models.reviewData import *
from models.userData import *
import os
import math
import boto3

key = os.getenv('JWT_SECRET_KEY')
key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')

client = boto3.client('s3',
                      aws_access_key_id=key_id,
                      aws_secret_access_key=secret_key
                      )


movie_database = MovieDatabase()
review_database = ReviewDatabase()
user_database = UserDatabase()


def up_load_to_s3(img, user_id):
    # 丟S3
    client.put_object(
        Bucket=bucket_name,
        Body=img,
        Key=f'userPic/userProfileImg-{user_id}.jpg',
        ContentType='image/jpeg',
    )


def make_review_dic(data):
    data_dic = {
        'data': []
    }

    for info in data:
        dic = {
            'review': info[4],
            'reviewDay': info[5],
            'watchedDay': info[6],
            'spoilers': info[7],
            'movieId': info[3],
            'filmTitle': info[0],
            'filmYear': info[1],
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


def get_user_review_func(review_id):
    data = review_database.get_review_by_review_id(review_id)
    if data[0] is None:
        return {'error': True,
                'message': 'Something is wrong, please try again'
                }
    review_data = data[0]
    rate_data = data[1]
    if rate_data is None:
        rate_data = None
    else:
        rate_data = rate_data[0]

    make_data_dic = {
        'data': {
            'movieId': review_data[1],
            'movieReview': review_data[2],
            'reviewDate': review_data[3],
            'watchedDate': review_data[4],
            'spoiler': review_data[5],
            'movieTitle': review_data[7],
            'movieYear': review_data[8],
            'movieRate': rate_data
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
def update_user_review_func(review_id, movie_review, watched_date, spoilers):
    review_updated = review_database.update_review(review_id, movie_review, watched_date, spoilers)
    if review_updated:
        return {
            'ok': True,
        }
    else:
        return{
            'error': True,
            'message': 'Something goes wrong, please try again'
        }


# delete user review
def delete_user_review_func(review_id):
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


def get_movies_user_likes_func(page_master):
    movies_user_likes = user_database.get_movies_user_likes(page_master, 21)
    if movies_user_likes is None:
        return {'error': True,
                'message': 'Oops, looks like there is no movie you like, go and find some?'}
    data = {
        'data': {
            'data':[]
        }
    }
    for movie in movies_user_likes:
        data['data']['data'].append(movie)

    return data


def get_reviews_user_likes_func(page_master):
    reviews_user_likes = user_database.get_reviews_user_likes(page_master, 8)
    if reviews_user_likes is None:
        return {'error': True,
                'message': 'Oops, looks like there is no review you like, go and find some?'}
    data = {
        'data': {
            'data': []
        }
    }
    for review in reviews_user_likes:
        info = {
            'reviewId': review[0],
            'reviewer': review[1],
            'reviewerImg': review[2],
            'movieId': review[3],
            'review': review[4],
            'spoilers': review[5],
            'movieTitle': review[6],
            'year': review[7]
        }
        data['data']['data'].append(info)

    return data


def get_all_movies_user_likes_func(page_master, page):
    page = int(page)
    all_movies_user_likes_count = user_database.count_all_movies_user_likes(page_master)
    all_movies_user_likes = user_database.get_movies_user_likes(page_master, 50)

    if all_movies_user_likes_count is not None:
        total_pages = math.ceil(int(all_movies_user_likes_count[0]) / 50)
        data = {
            'data': {
                'data': [],
                'nextPage': None,
                'totalPages': total_pages
            }
        }
        if page < total_pages:
            data['data']['nextPage'] = page+1
        for movie in all_movies_user_likes:
            data['data']['data'].append(movie)
        return data
    else:
        return {'error': True}


def get_all_reviews_user_likes_func(page_master, page):
    page = int(page)
    all_reviews_user_likes_count = user_database.count_all_movies_user_likes(page_master)
    all_reviews_user_likes = user_database.get_reviews_user_likes(page_master, 20)

    if all_reviews_user_likes_count is not None:
        total_pages = math.ceil(int(all_reviews_user_likes_count[0]) / 50)
        data = {
            'data': {
                'data': [],
                'nextPage': None,
                'totalPages': total_pages
            }
        }
        if page < total_pages:
            data['data']['nextPage'] = page + 1
        for review in all_reviews_user_likes:
            info = {
                'reviewId': review[0],
                'reviewer': review[1],
                'reviewerImg': review[2],
                'movieId': review[3],
                'review': review[4],
                'spoilers': review[5],
                'movieTitle': review[6],
                'year': review[7],
                'reviewDate': review[8]
            }
            data['data']['data'].append(info)
        return data
    else:
        return {'error': True}


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
            'error': True,
            'message': 'Something went wrong, please try again'
        }


def get_user_profile_pic_func(user_name):
    user_profile_pic_name = user_database.get_user_profile_pic(user_name)
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


# watchlist
# get watchlist
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
            'totalMovies': movies_in_watchlist
        }
    }
    for movie in watchlist:
        data['data']['data'].append(movie)
    data = make_page(data, page, total_page)
    return data