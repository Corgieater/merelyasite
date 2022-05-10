from controllers.search import *
from flask import *

search_Blueprint = Blueprint(
    'search_Blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@search_Blueprint.route('/api/search')
def search():
    user_keyword = request.args.get('keyword')
    user_page = request.args.get('page')
    print(user_keyword)
    print(user_page)
    return get_info_func(user_keyword, user_page)


@search_Blueprint.route('/search')
def redirect_to_search_page():
    return render_template('searchResults.html')

