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
    results = get_info_func(user_input)
    if len(results) == 0:
        return {
            'error': True,
            'message': 'No such key word, please try another'
        }
    else:
        return results

@search_Blueprint.route('/search/<user_input>')
def redirect_to_search_page(user_input):
    return render_template('searchResults.html')
