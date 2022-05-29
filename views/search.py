from controllers.search import *
from flask import *

search_blueprint = Blueprint(
    'search_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# http://localhost:3000/search?keyword=&page=1
# 網頁右上角的搜尋from OK
@search_blueprint.route('/api/search')
def search():
    user_keyword = request.args.get('keyword')
    user_page = request.args.get('page')
    print(user_keyword)
    print(user_page)
    return get_info_func(user_keyword, user_page)


@search_blueprint.route('/search')
def render_search_page():
    return render_template('searchResults.html')


# 找導演
@search_blueprint.route('/api/search/director')
def get_director():
    director = request.args.get('director').replace('+', ' ')
    page = request.args.get('page')
    if page is None:
        page = 1
    return get_data_by_type_func(director, page, 'director')


# 找導演page render(有可愛logo那個)
@search_blueprint.route('/search/director')
def render_search_Director_page():
    director = request.args.get('director').replace('+', ' ')
    return render_template('searchDirector.html', director=director)


# 找演員
@search_blueprint.route('/api/search/actor')
def get_actor():
    actor = request.args.get('actor').replace('+', ' ')
    page = request.args.get('page')
    if page is None:
        page = 1
    return get_data_by_type_func(actor, page, 'actor')


# 找演員 page render(有可愛logo那個)
@search_blueprint.route('/search/actor')
def render_search_actor_page():
    actor = request.args.get('actor').replace('+', ' ')
    return render_template('searchActor.html', actor=actor)
