from controllers.userProfile import *
from flask import *

user_profile_blueprint = Blueprint(
    'user_profile',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# render template
@user_profile_blueprint.route('/user_profile/<user_name>')
def render_user_profile(user_name):
    return render_template('userProfile.html', name=user_name)


# 拿最新的五個評論
@user_profile_blueprint.route('/api/get_latest_reviews/<user_name>')
def get_user_latest_five_reviews(user_name):
    print(user_name)
    return get_user_latest_five_reviews_func(user_name)


# @user_profile_blueprint.route('/api/user_profile')
# def search_by_id(film_id):
#     return get_film_by_id_func(film_id)

@user_profile_blueprint.route('/setting')
def render_setting_page():
    return render_template('userSetting.html')
