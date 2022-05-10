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
