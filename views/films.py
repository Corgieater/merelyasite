from controllers.films import *
from flask import *
from controllers.crawler import *

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


# 拿這週最熱門的電影 *6 for index
@films_blueprint.route('/api/get_most_popular_movies_this_week/')
def get_most_popular_movies_this_week():
    return get_most_popular_movies_this_week_func()
