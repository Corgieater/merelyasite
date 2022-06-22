from controllers.userProfile import *
from flask import *

user_profile_blueprint = Blueprint(
    'user_profile',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# render user profile template
@user_profile_blueprint.route('/user_profile/<user_name>')
def render_user_profile(user_name):
    user_name = user_name.replace('+', ' ')
    return render_template('userProfile.html', name=user_name)


# 拿最新的五個評論for user page
@user_profile_blueprint.route('/api/user_latest_reviews/<user_name>')
def get_user_latest_five_reviews(user_name):
    user_name = user_name.replace('+', ' ')
    return get_user_latest_five_reviews_func(user_name)


# 照頁數拿所有評論for user page
@user_profile_blueprint.route('/api/reviews_by_page/<user_name>/reviews')
def get_reviews_by_page(user_name):
    user_name = user_name.replace('+', ' ')
    page = request.args.get('page')
    if page is None:
        page = 1
    return get_reviews_by_page_func(user_name, page)


# render user profile reviews page
@user_profile_blueprint.route('/user_profile/<user_name>/reviews')
def render_user_profile_reviews(user_name):
    return render_template('userProfileReviews.html')


# get user review
@user_profile_blueprint.route('/api/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>',
                              methods=['GET'])
def get_user_review(user_name, movie_name, review_id):
    return get_user_review_func(review_id)


# update user review
@user_profile_blueprint.route('/api/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>',
                              methods=['PATCH'])
def update_user_review(user_name, movie_name, review_id):
    data = request.get_json()
    movie_review = data['movieReview']
    watched_date = data['watchedDate']
    spoilers = data['spoilers']
    return update_user_review_func(review_id, movie_review, watched_date, spoilers)


# delete review
@user_profile_blueprint.route('/api/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>',
                              methods=['DELETE'])
def delete_user_review(user_name, movie_name, review_id):
    return delete_user_review_func(review_id)


# render user profile review each
@user_profile_blueprint.route('/user_profile/<user_name>/reviews/films/<movie_name>/<review_id>')
def render_user_profile_reviews_each(user_name, movie_name, review_id):
    user_name = user_name.replace('+', ' ')
    return render_template('userProfileReviewsEach.html', userName=user_name)


# render user setting
@user_profile_blueprint.route('/setting')
def render_setting_page():
    return render_template('userSetting.html')


# user profile 上傳圖片
@user_profile_blueprint.route('/api/user/<user_id>/pic', methods=["PATCH"])
def upload_user_profile_pic(user_id):
    img = request.files['photoFile']
    return upload_user_profile_pic_func(user_id, img)


# page master profile 拿該頁面擁有者的上傳照片 沒有就用預設
@user_profile_blueprint.route('/api/user/<user_name>/pic')
def get_user_profile_pic(user_name):
    user_name = user_name.replace('+', ' ')
    return get_user_profile_pic_func(user_name)


# render watchlist
@user_profile_blueprint.route('/user_profile/<page_master>/watchlist')
def render_user_watchlist_page(page_master):
    page_master = page_master.replace('+', ' ')

    return render_template('userWatchlist.html', pageMaster=page_master)


# 拿watchlist
@user_profile_blueprint.route('/api/user_profile/<page_master>/watchlist')
def get_watchlist_by_page(page_master):
    page_master = page_master.replace('+', ' ')
    page = request.args.get('page')

    return get_watchlist_by_page_func(page_master, page)


# render user profile likes頁面
@user_profile_blueprint.route('/user_profile/<page_master>/likes')
def render_user_likes_page(page_master):
    page_master = page_master.replace('+', ' ')
    return render_template('userLikes.html', pageMaster=page_master)


# get all movies user likes for user profile
@user_profile_blueprint.route('/api/user_profile/<page_master>/likes/allMovies')
def get_all_movies_user_likes(page_master):
    page_master = page_master.replace('+', ' ')
    page = request.args.get('page')
    return get_all_movies_user_likes_func(page_master, page)


# render user profile all movies user likes頁面
@user_profile_blueprint.route('/user_profile/<page_master>/likes/allMovies')
def render_movies_user_likes_page(page_master):
    return render_template('moviesUserLikes.html')


# get all reviews user likes for user profile
@user_profile_blueprint.route('/api/user_profile/<page_master>/likes/allReviews')
def get_all_reviews_user_likes(page_master):
    page_master = page_master.replace('+', ' ')
    page = request.args.get('page')
    return get_all_reviews_user_likes_func(page_master, page)


# render user profile all reviews user likes頁面
@user_profile_blueprint.route('/user_profile/<page_master>/likes/allReviews')
def render_reviews_user_likes_page(page_master):
    return render_template('reviewsUserLikes.html')


# get movies user like
@user_profile_blueprint.route('/api/user_profile/<page_master>/likes/movies')
def get_movies_user_likes(page_master):
    page_master = page_master.replace('+', ' ')
    return get_movies_user_likes_func(page_master)


# get reviews user like
@user_profile_blueprint.route('/api/user_profile/<page_master>/likes/reviews')
def get_reviews_user_likes(page_master):
    page_master = page_master.replace('+', ' ')
    return get_reviews_user_likes_func(page_master)
