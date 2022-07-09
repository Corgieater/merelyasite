from controllers.auth import *
from controllers.social import *
from controllers.userGeneral import *
from flask import flash

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


# 驗證email
@user_blueprint.route('/api/user/validation/<auth_token>')
def user_validate_func(auth_token):
    print('someone reached validation api,', auth_token)
    email_confirmed = confirm_token(auth_token)
    if email_confirmed:
        flash('Your email had been verified!', 'good')
        return redirect('/')
    else:
        return redirect('/user/validation')


# validation token失效 要重新填帳號密碼重寄
@user_blueprint.route('/user/validation')
def auth_token_expired():
    return render_template('authTokenExpired.html')


# check user name if available
@user_blueprint.route('/api/user/<sign_up_name>')
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
