from controllers.search import *
from flask import *

search_Blueprint = Blueprint(
    'search_Blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@search_Blueprint.route('/api/search/<user_input>')
def search(user_input):
    return get_info_func(user_input)


@search_Blueprint.route('/search/<user_input>')
def redirect_to_search_page(user_input):
    return render_template('searchResults.html')

