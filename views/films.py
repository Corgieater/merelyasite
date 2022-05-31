from controllers.films import *
from flask import *
from controllers.getMovie import *


films_blueprint = Blueprint(
    'films_Blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# 導演演員的確定路徑(全名)一定要是類似這樣
#  https://letterboxd.com/actor/tom-cruise/
# 顯示電影的方式就用下滑打API

# ID搜電影 OK
@films_blueprint.route('/api/film/<film_id>')
def search_by_id(film_id):
    return get_film_by_id_func(film_id)


# render template ID
@films_blueprint.route('/film/<film_id>')
def render_film_page(film_id):
    return render_template('film.html')

# # 找導演
# @films_blueprint.route('/api/search/director')
# def get_director():
#     director = request.args.get('director').replace('+', ' ')
#     page = request.args.get('page')
#     if page is None:
#         page = 1
#     return get_data_by_type_func(director, page, 'director')
#
#
# # render search director page
# @films_blueprint.route('/search/director')
# def render_search_Director_page():
#     director = request.args.get('director').replace('+', ' ')
#     return render_template('searchDirector.html', director=director)


# # 找演員
# @films_blueprint.route('/api/search/actor')
# def get_actor():
#     actor = request.args.get('actor').replace('+', ' ')
#     page = request.args.get('page')
#     if page is None:
#         page = 1
#     return get_data_by_type_func(actor, page, 'actor')
#
#
# # render search actor page
# @films_blueprint.route('/search/actor')
# def render_search_actor_page():
#     actor = request.args.get('actor').replace('+', ' ')
#     return render_template('searchActor.html', director=actor)


# director搜電影 OK
@films_blueprint.route('/api/director')
def search_by_director():
    director = request.args.get('director').replace('+', ' ')
    print('director', director)
    page = request.args.get('page')
    print(page)
    if page is None:
        page = 1
    return get_films_by_director_func(director, page)

# render template director
@films_blueprint.route('/director')
def render_director_page():
    #參數沒用到還是要填
    director = request.args.get('director').replace('+', ' ')
    return render_template('director.html', director=director)


# 演員搜電影 OK
@films_blueprint.route('/api/actor')
def search_by_actor():
    actor = request.args.get('actor')
    print(actor)
    page = request.args.get('page')
    print(page)
    if page is None:
        page = 1
    actor = actor.replace('+', ' ')
    print(actor, 'after replace')
    return get_films_by_actor_func(actor, page)

# render template actor
@films_blueprint.route('/actor')
def render_actor_page():
    actor = request.args.get('actor').replace('+', ' ')
    return render_template('actor.html', actor=actor)


# genre搜電影 HERE--------------------
# @films_blueprint.route('/api/genre')
# def search_by_genre():
#     genre = request.args.get('genre')
#     page = request.args.get('page')
#     print('genre', genre, page)
#     return get_films_by_genre_func(genre, page)
#
#
# # render template genre
# @films_blueprint.route('/genre')
# def render_genre_page():
#     return render_template('genre.html')


# 評分 HERE
@films_blueprint.route('/api/rate', methods=['PATCH'])
def rating():
    data = request.get_json()
    print(data)
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
        return rating_func(rate, user_id, film_id)


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


# 寫評論
@films_blueprint.route('/api/review', methods=['PATCH'])
def film_review():
    data = request.get_json()
    movie_review = data['movieReview']
    film_id = data['filmId']
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
            print('from place', from_place)
            return film_review_func\
                (movie_review, film_id, current_date, watched_date, user_id, spoilers,
                 review_id=review_id, from_where=from_place)
    # 如果沒填review id = 從film來的
    except KeyError:
        return film_review_func(movie_review, film_id, current_date, watched_date, user_id, spoilers)


# nav 上的films
@films_blueprint.route('/films')
def render_films_page():
    return render_template('publicFilms.html')

# 加入電影   ****************要修 想辦法去爬IMDB 不然 TAGLINE就爆了
@films_blueprint.route('/api/addFilm')
def get_movie_from_omdb():
    title = request.args.get('t').replace('+', ' ')
    year = request.args.get('y')
    add_to_database = get_movie_from_omdb_func(title, year)
    if add_to_database:
        return {'ok': True}
    else:
        return {'error': True,
                'message': 'Movie already exist'}


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