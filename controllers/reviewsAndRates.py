from models.reviewData import *
review_database = ReviewDatabase()


# 更新或加入評分
def rating_func(rate, user_id, film_id):
    if user_id is None:
        return {
            'error': True,
            'message': 'Please log in'
        }
    result = review_database.rating(rate, user_id, film_id)
    if result is True:
        return {'ok': True}

    else:
        return{
            'error': 'Something went wrong, please try again'
        }


# 拿上次評分
def get_rate_func(user_id, movie_id):
    rate = review_database.get_rate_data(user_id, movie_id)
    if rate:
        data = {
            'data': {'rate': rate}
        }
        return data
    else:
        return {
            'data': {'rate': None}
        }


# 刪除評分
def delete_rate_func(film_id, user_id):
    data_deleted = review_database.delete_rate_data(film_id, user_id)
    if data_deleted:
        return {
            'ok': True
        }
    else:
        return{
            'error': False,
            'message': 'Deleting failed, please try again'
        }


# 拿均分
def get_average_rate_func(film_id):
    data = review_database.get_average_rate_data(film_id)

    if data:
        return {
            'data': {'totalCount': data[0],'average':data[1]}
        }
    else:
        return {
            'error': False
        }


# 評論相關
# 留評論
def film_review_func(movie_review, film_id, current_date, watched_date, user_id, spoilers,
                     review_id=None, from_where=None):
    if from_where == 'userProfileReviewAgain':
        movie_and_user_id = review_database.get_movie_id_and_user_id_for_review_again(review_id)
        film_id = movie_and_user_id[0]
        user_id = movie_and_user_id[1]
        if user_id is None and from_where is None:
            return {
                'error': True,
                'message': 'Please log in'
            }
        result = review_database.write_review(movie_review, film_id, current_date, watched_date, user_id, spoilers)
    else:
        result = review_database.write_review(movie_review, film_id, current_date, watched_date, user_id, spoilers)

    if result is True:
        return {
            'ok': True
        }
    else:
        return {
            'error': False,
            'message': 'Review failed, please try again'
        }


# for index
def get_latest_reviews_func():
    latest_reviews = review_database.get_latest_reviews_for_index()
    total_reviews = review_database.get_all_reviews_count()
    data = {
        'data': {'data': [],'totalReviews': total_reviews[0]}
    }
    for reviews in latest_reviews:
        info = {
            'userName': reviews[0],
            'reviewMovie': reviews[1],
            'reviewId': reviews[2],
            'reviewMovieId': reviews[3],

        }
        data['data']['data'].append(info)

    return data
