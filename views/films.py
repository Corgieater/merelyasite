from controllers.films import *
from flask import *
from controllers.getMovie import *

films_blueprint = Blueprint(
    'films_Blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# ID拿電影
@films_blueprint.route('/api/film/<film_id>')
def get_movie_by_id(film_id):
    return get_movie_by_id_func(film_id)


# render template film.html 電影頁面
@films_blueprint.route('/film/<film_id>')
def render_film_page(film_id):
    return render_template('film.html')


# director拿電影
@films_blueprint.route('/api/director')
def get_movies_by_director():
    director = request.args.get('director').replace('+', ' ')
    page = request.args.get('page')
    if page is None:
        page = 1
    return get_movies_by_director_func(director, page)


# render template 導演所有電影頁面
@films_blueprint.route('/director')
def render_director_page():
    director = request.args.get('director').replace('+', ' ')
    return render_template('director.html', director=director)


# 演員拿電影
@films_blueprint.route('/api/actor')
def get_movies_by_actor():
    actor = request.args.get('actor')
    page = request.args.get('page')
    if page is None:
        page = 1
    actor = actor.replace('+', ' ')
    return get_movies_by_actor_func(actor, page)


# render template actor 演員所有電影頁面
@films_blueprint.route('/actor')
def render_actor_page():
    actor = request.args.get('actor').replace('+', ' ')
    return render_template('actor.html', actor=actor)


# # 評分
# @films_blueprint.route('/api/rate', methods=['PATCH'])
# def rating():
#     data = request.get_json()
#     try:
#         rate = data['rate']
#         user_id = data['userId']
#         film_id = data['movieId']
#     except Exception as e:
#         print(e)
#         return {
#             'data': {'error': True,
#                      'message': 'Please log in'}
#         }
#     else:
#         return rating_func(rate, user_id, film_id)
#
#
# # 拿使用者上次評分
# @films_blueprint.route('/api/rate/<user_id>/<film_id>')
# def get_rate(user_id, film_id):
#     return get_rate_func(user_id, film_id)
#
#
# # 刪評分
# @films_blueprint.route('/api/rate', methods=['DELETE'])
# def delete_rate():
#     data = request.get_json()
#     film_id = data['movieId']
#     user_id = data['userId']
#
#     return delete_rate_func(film_id, user_id)
#
#
# # 拿電影均分
# @films_blueprint.route('/api/average-rate', methods=['POST'])
# def get_average_rate():
#     data = request.get_json()
#     film_id = data['movieId']
#
#     return get_average_rate_func(film_id)
#
#
# # 寫評論
# @films_blueprint.route('/api/review', methods=['PATCH'])
# def film_review():
#     data = request.get_json()
#     movie_review = data['movieReview']
#     film_id = data['movieId']
#     current_date = data['currentDate']
#     watched_date = data['watchedDate']
#     if watched_date is None:
#         watched_date = None
#     user_id = data['userId']
#     spoilers = data['spoilers']
#     try:
#         if data['reviewId']:
#             review_id = data['reviewId']
#             from_place = data['from']
#             return film_review_func \
#                 (movie_review, film_id, current_date, watched_date, user_id, spoilers,
#                  review_id=review_id, from_where=from_place)
#     # 如果沒填review id = 從film來的
#     except KeyError:
#         return film_review_func(movie_review, film_id, current_date, watched_date, user_id, spoilers)


# nav 上的films render films page
@films_blueprint.route('/films')
def render_films_page():
    return render_template('publicFilms.html')


# 加入電影
@films_blueprint.route('/api/addFilm')
def get_movie_from_imdb():
    title = request.args.get('t').replace('+', ' ')
    year = request.args.get('y')
    try:
        year = int(year)
    except Exception as e:
        print(e)
        return {'error': True,
                'message': 'Please type valid year'}
    return get_movie_from_imdb_func(title, year)


# # 拿最新的12個評論 from index
# @films_blueprint.route('/api/get_latest_reviews/')
# def get_latest_reviews():
#     return get_latest_reviews_func()


# 拿這週最熱門的電影 *6 for index
@films_blueprint.route('/api/get_most_popular_movies_this_week/')
def get_most_popular_movies_this_week():
    return get_most_popular_movies_this_week_func()
