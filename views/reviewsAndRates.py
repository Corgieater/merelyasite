from controllers.reviewsAndRates import *
from flask import *


reviewsAndRates_blueprint = Blueprint(
    'reviewsAndRates_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# 評分
@reviewsAndRates_blueprint.route('/api/rate', methods=['PATCH'])
def rating():
    data = request.get_json()
    try:
        rate = data['rate']
        user_id = data['userId']
        film_id = data['movieId']
    except Exception as e:
        print(e)
        return {
            'data': {'error': True,
                     'message': 'Please log in'}
        }
    else:
        return rating_func(rate, user_id, film_id)


# 拿使用者上次評分
@reviewsAndRates_blueprint.route('/api/rate/<user_id>/<film_id>')
def get_rate(user_id, film_id):
    return get_rate_func(user_id, film_id)


# 刪評分
@reviewsAndRates_blueprint.route('/api/rate', methods=['DELETE'])
def delete_rate():
    data = request.get_json()
    movie_id = data['movieId']
    user_id = data['userId']

    return delete_rate_func(movie_id, user_id)


# 拿電影均分
@reviewsAndRates_blueprint.route('/api/average-rate', methods=['POST'])
def get_average_rate():
    data = request.get_json()
    movie_id = data['movieId']

    return get_average_rate_func(movie_id)


# 寫評論
@reviewsAndRates_blueprint.route('/api/review', methods=['PATCH'])
def film_review():
    data = request.get_json()
    movie_review = data['movieReview']
    film_id = data['movieId']
    current_date = data['currentDate']
    watched_date = data['watchedDate']
    if watched_date is None:
        watched_date = None
    user_id = data['userId']
    spoilers = data['spoilers']
    try:
        if data['reviewId']:
            review_id = data['reviewId']
            from_place = data['from']
            return film_review_func \
                (movie_review, film_id, current_date, watched_date, user_id, spoilers,
                 review_id=review_id, from_where=from_place)
    # 如果沒填review id = 從film來的
    except KeyError:
        return film_review_func(movie_review, film_id, current_date, watched_date, user_id, spoilers)


# 拿最新的12個評論 from index
@reviewsAndRates_blueprint.route('/api/get_latest_reviews/')
def get_latest_reviews():
    return get_latest_reviews_func()
