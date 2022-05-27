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
    user_name = user_name.replace('+', ' ')
    return render_template('userProfile.html', name=user_name)


# 拿最新的五個評論
@user_profile_blueprint.route('/api/get_latest_reviews/<user_name>')
def get_user_latest_five_reviews(user_name):
    user_name = user_name.replace('+', ' ')
    print(user_name)
    return get_user_latest_five_reviews_func(user_name)


# 照頁數拿所有評論
@user_profile_blueprint.route('/api/get_reviews_by_page/<user_name>/reviews')
def get_reviews_by_page(user_name):
    user_name = user_name.replace('+', ' ')
    print(user_name)
    page = request.args.get('page')
    if page is None:
        page = 1
    return get_reviews_by_page_func(user_name, page)

# render user profile reviews page
@user_profile_blueprint.route('/user_profile/<user_name>/reviews')
def render_user_profile_reviews(user_name):
    return render_template('userProfileReviews.html')

# @user_profile_blueprint.route('/api/user_profile')
# def search_by_id(film_id):
#     return get_film_by_id_func(film_id)

@user_profile_blueprint.route('/setting')
def render_setting_page():
    return render_template('userSetting.html')
