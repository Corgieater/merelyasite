from controllers.films import *
from flask import *
from controllers.getMovie import *


# from moviePro.spiders import movieSpy
# from scrapy.crawler import CrawlerProcess
# from scrapy.settings import Settings
# from moviePro import settings as my_settings





films_blueprint = Blueprint(
    'films_Blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# ID搜電影
@films_blueprint.route('/api/film/<film_id>')
def search_by_id(film_id):
    return get_film_by_id_func(film_id)


# render template ID
@films_blueprint.route('/film/<film_id>')
def render_film_page(film_id):
    return render_template('film.html')


# director搜電影
@films_blueprint.route('/api/director/<director>')
def search_by_director(director):
    print(director.replace('+', ' '))
    director = director.replace('+', ' ')
    return get_film_by_director(director)


# render template director
@films_blueprint.route('/director/<director>')
def render_director_page(director):
    return render_template('director.html')


# 評分
@films_blueprint.route('/api/rate', methods=['PATCH'])
def renew_rate():
    data = request.get_json()
    try:
        rate = data['rate']
        user_id = data['userId']
        film_id = data['filmId']
    except Exception as e:
        print(e)
        return {
            'data': {'error': True,
                     'message': 'Please log in'}
        }
    else:
        return renew_rate_func(rate, user_id, film_id)


# 拿使用者上次評分
@films_blueprint.route('/api/rate', methods=['POST'])
def get_rate():
    data = request.get_json()
    try:
        user_id = data['userId']
        film_id = data['filmId']
    except Exception as e:
        print(e)
        return {
            'data': {'rate': None}
        }
    else:
        return get_rate_func(user_id, film_id)


# 刪評分
@films_blueprint.route('/api/rate', methods=['DELETE'])
def delete_rate():
    data = request.get_json()
    print("films_blueprint.route('/api/rate', methods=['DELETE']", data)
    film_id = data['filmId']
    user_id = data['userId']

    return delete_rate_func(film_id, user_id)


# 拿電影均分
@films_blueprint.route('/api/average-rate', methods=['POST'])
def get_average_rate():
    data = request.get_json()
    film_id = data['filmId']

    return get_average_rate_func(film_id)


# 寫/更新評論 寫到使用者頁面的時候回頭來寫
@films_blueprint.route('/api/review', methods=['PATCH'])
def film_review():
    data = request.get_json()
    user_review = data['userReview']
    film_id = data['filmId']
    current_date = data['currentDate']
    watched_date = data['watchedDate']
    if watched_date is None:
        watched_date = None
    user_id = data['userId']

    return film_review_func(user_review, film_id, current_date, watched_date, user_id)


# 刪評論 *********** 寫到使用者頁面的時候回頭來檢查
@films_blueprint.route('/api/review', methods=['DELETE'])
def film_delete():
    data = request.get_json()
    print(data)
    film_id = data['filmId']
    user_id = data['userId']

    return film_delete_func(film_id, user_id)


# nav 上的films
@films_blueprint.route('/films')
def render_films_page():
    return render_template('publicFilms.html')


@films_blueprint.route('/api/addFilm')
def get_movie_from_omdb():
    title = request.args.get('t').replace('+', ' ')
    year = request.args.get('y')
    add_to_database = get_movie_from_omdb_func(title, year)
    if add_to_database:
        return {'ok': True}
    else:
        return {'error': True,
                'message': 'Something went wrong, please try again'}


# 修改評論
# ***********************
# @films_blueprint.route('/api/edit-review', methods=['PATCH'])
# def film_review():
#     data = request.get_json()
#     print(data)
#     user_review = data['userReview']
#     film_id = data['filmId']
#     current_date = data['currentDate']
#     watched_date = data['watchedDate']
#     if watched_date is None:
#         watched_date = None
#     user_id = data['userId']
#
#     return film_edit_func(user_review, film_id, current_date, watched_date, user_id)