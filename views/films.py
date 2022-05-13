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


# 評分
@films_blueprint.route('/api/rate', methods=['PATCH'])
def renew_rate():
    data = request.get_json()
    rate = data['rate']
    user_id = data['userId']
    film_id = data['filmId']

    return renew_rate_func(rate, user_id, film_id)

# 拿使用者上次評分
@films_blueprint.route('/api/rate', methods=['POST'])
def get_rate():
    data = request.get_json()
    user_id = data['userId']
    film_id = data['filmId']

    return get_rate_func(user_id, film_id)

# 刪評分
@films_blueprint.route('/api/rate', methods=['DELETE'])
def delete_rate():
    data = request.get_json()
    user_id = data['userId']
    film_id = data['filmId']

    return delete_rate_func(user_id, film_id)


# 寫/更新評論 寫到使用者頁面的時候回頭來寫
@films_blueprint.route('/api/review', methods=['PATCH'])
def film_review():
    data = request.get_json()
    print(data)
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