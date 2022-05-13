from controllers.userProfile import *
from flask import *

user_profile_blueprint = Blueprint(
    'user_profile',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@user_profile_blueprint.route('/user_profile')
def render_user_profile():
    return render_template('userProfile.html')


# @user_profile_blueprint.route('/api/user_profile')
# def search_by_id(film_id):
#     return get_film_by_id_func(film_id)