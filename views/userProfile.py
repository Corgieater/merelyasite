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


# get user's own review
@user_profile_blueprint.route('/api/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>',
                              methods=['GET'])
def get_user_profile_review_each(user_name, movie_name, review_id):
    user_name = user_name.replace('+', ' ')
    print(user_name, movie_name, review_id, 'from get use profile review each views')
    return get_user_profile_review_each_func(user_name,review_id)


# update user review
@user_profile_blueprint.route('/api/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>',
                              methods=['PATCH'])
def update_user_profile_review(user_name, movie_name, review_id):
    data = request.get_json()
    print(data)
    movie_review = data['movieReview']
    watched_date = data['watchedDate']
    spoilers = data['spoilers']
    return update_user_profile_review_func(review_id, movie_review, watched_date, spoilers)

# # review again func 要怎麼改呢??
# @user_profile_blueprint.route('/api/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>',
#                               methods=['PATCH'])
# def user_profile_review_again(user_name, movie_name, review_id):
#     data = request.get_json()
#     print(data)
#     movie_review = data['movieReview']
#     watched_date = data['watchedDate']
#     spoilers = data['spoilers']
#     return user_profile_review_again_func(review_id, movie_review, watched_date, spoilers)


# delete review
@user_profile_blueprint.route('/api/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>',
                              methods=['DELETE'])
def delete_user_profile_review(user_name, movie_name, review_id):
    return delete_user_profile_review_func(review_id)

# render user profile review each
@user_profile_blueprint.route('/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>')
def render_user_profile_reviews_each(user_name, movie_name, review_id):
    user_name = user_name.replace('+', ' ')
    return render_template('userProfileReviewsEach.html', userName=user_name)

# @user_profile_blueprint.route('/api/user_profile')
# def search_by_id(film_id):
#     return get_film_by_id_func(film_id)

@user_profile_blueprint.route('/setting')
def render_setting_page():
    return render_template('userSetting.html')

