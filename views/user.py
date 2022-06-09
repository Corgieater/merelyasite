from controllers.auth import *
from controllers.social import *
from controllers.userProfile import *

user_blueprint = Blueprint(
    'user_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# 登入登出相關
# sign up
@user_blueprint.route('/api/user', methods=['POST'])
def sign_up_func():
    data = request.get_json()
    return sign_up(data['email'], data['password'], data['name'])


# check user name if available
@user_blueprint.route('/api/user/<sign_up_name>',)
def check_user_name(sign_up_name):
    sign_up_name = sign_up_name.replace('+', ' ')
    return check_user_name_func(sign_up_name)


# 登入
@user_blueprint.route('/api/user', methods=['PATCH'])
def log_in_func():
    data = request.get_json()
    return log_in(data['email'], data['password'])


# 確認user登入狀態
@user_blueprint.route('/api/user', methods=["GET"])
def check_user_func():
    return user_checker()


# 登出
@user_blueprint.route('/api/user', methods=["DELETE"])
def sign_out_func():
    return sign_out()


# user自己的功能
# render watchlist
@user_blueprint.route('/user_profile/<page_master>/watchlist')
def render_user_watchlist_page(page_master):
    page_master = page_master.replace('+', ' ')

    return render_template('userWatchlist.html', pageMaster=page_master)


# 拿watchlist
@user_blueprint.route('/api/user_profile/<page_master>/watchlist')
def get_watchlist_by_page(page_master):
    page_master = page_master.replace('+', ' ')
    page = request.args.get('page')

    return get_watchlist_by_page_func(page_master, page)


# 看該使用者有沒有把這電影加入watchlist/movies likes
@user_blueprint.route('/api/user_profile/user_movie_state/<user_id>/<movie_id>')
def check_user_movie_state(user_id, movie_id):
    return check_user_movie_state_func(user_id, movie_id)


# /api/user_profile/user_review_state
# 看該使用者有沒有把這review加入reviews likes 決定跟上面分開是因為film沒有review
@user_blueprint.route('/api/user_profile/user_review_state/<user_id>/<review_id>')
def user_review_state(user_id, review_id):
    return check_user_review_likes(user_id, review_id)


# 加入待看清單watchlist
@user_blueprint.route('/api/user_profile/watchlist', methods=["PATCH"])
def add_movie_to_watchlist():
    data = request.get_json()
    movie_id = data['movieId']
    user_id = data['userId']
    return add_movie_to_watchlist_func(user_id, movie_id)


# delete from watchlist
@user_blueprint.route('/api/user_profile/watchlist', methods=["DELETE"])
def delete_movie_from_watchlist():
    data = request.get_json()
    movie_id = data['movieId']
    user_id = data['userId']
    return delete_movie_from_watchlist_func(user_id, movie_id)


# render user profile likes頁面
@user_blueprint.route('/user_profile/<page_master>/likes')
def render_user_likes_page(page_master):
    page_master = page_master.replace('+', ' ')
    return render_template('userLikes.html', pageMaster=page_master)


# get all movies user likes for user profile
@user_blueprint.route('/api/user_profile/<page_master>/likes/allMovies')
def get_all_movies_user_likes(page_master):
    page_master = page_master.replace('+', ' ')
    page = request.args.get('page')
    return get_all_movies_user_likes_func(page_master, page)


# render user profile all movies user likes頁面
@user_blueprint.route('/user_profile/<page_master>/likes/allMovies')
def render_movies_user_likes_page(page_master):
    return render_template('moviesUserLikes.html')


# get all reviews user likes for user profile
@user_blueprint.route('/api/user_profile/<page_master>/likes/allMovies')
def get_all_reviews_user_likes(page_master):
    page_master = page_master.replace('+', ' ')
    return get_all_reviews_user_likes_func(page_master)


# render user profile all reviews user likes頁面
@user_blueprint.route('/user_profile/<page_master>/likes/allReviews')
def render_reviews_user_likes_page(page_master):
    return render_template('reviewsUserLikes.html')


# get movies user like
@user_blueprint.route('/api/user_profile/<page_master>/likes/movies')
def get_movies_user_likes(page_master):
    page_master = page_master.replace('+', ' ')
    return get_movies_user_likes_func(page_master)


# get reviews user like
@user_blueprint.route('/api/user_profile/<page_master>/likes/reviews')
def get_reviews_user_likes(page_master):
    page_master = page_master.replace('+', ' ')
    return get_reviews_user_likes_func(page_master)


# 加入likes_movies 喜歡這個電影
@user_blueprint.route('/api/user_profile/likes/movie', methods=["PATCH"])
def add_movie_to_likes():
    data = request.get_json()
    movie_id = data['movieId']
    user_id = data['userId']
    return add_movie_to_likes_func(user_id, movie_id)


# delete movies user likes
@user_blueprint.route('/api/user_profile/likes/movie', methods=["DELETE"])
def delete_movie_from_likes():
    data = request.get_json()
    movie_id = data['movieId']
    user_id = data['userId']
    return delete_movie_from_likes_func(user_id, movie_id)


# user profile 上傳圖片
@user_blueprint.route('/api/user/<user_id>/upload_pic', methods=["PATCH"])
def upload_user_profile_pic(user_id):
    img = request.files['photoFile']
    return upload_user_profile_pic_func(user_id, img)


# page master profile 拿該頁面擁有者的上傳照片 沒有就用預設
@user_blueprint.route('/api/user/<user_name>/upload_pic')
def get_user_profile_pic(user_name):
    user_name = user_name.replace('+', ' ')
    return get_user_profile_pic_func(user_name)

