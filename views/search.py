from controllers.search import *
from flask import *

search_blueprint = Blueprint(
    'search_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


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

