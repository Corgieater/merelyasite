from controllers.films import *
from flask import *

films_blueprint = Blueprint(
    'films_Blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@films_blueprint.route('/api/film/<film_id>')
def search_by_id(film_id):
    return get_film_by_id_func(film_id)


@films_blueprint.route('/film/<film_id>')
def render_film_page(film_id):
    return render_template('film.html')


# 寫心得
@films_blueprint.route('/api/film/review', methods=['PATCH'])
def write_review():
    return write_review_func()

# 評分


@films_blueprint.route('/api/rate', methods=['PATCH'])
def renew_rate():
    data = request.get_json()
    rate = data['rate']
    user_id = data['userId']
    movie_id = data['movieId']

    return renew_rate_func(rate, user_id, movie_id)


@films_blueprint.route('/api/rate', methods=['GET'])
def get_rate():
    data = request.get_json()
    user_id = data['userId']
    movie_id = data['movieId']
    # 回傳分數做一做喔
    return get_rate_func(user_id, movie_id)
