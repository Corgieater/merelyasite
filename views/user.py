from controllers.auth import *
from controllers.social import *

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


# check user name available
@user_blueprint.route('/api/user/<sign_up_name>',)
def check_user_name(sign_up_name):
    sign_up_name = sign_up_name.replace('+', ' ')
    print(sign_up_name)
    return check_user_name_func(sign_up_name)

@user_blueprint.route('/api/user', methods=['PATCH'])
def log_in_func():
    data = request.get_json()
    return log_in(data['email'], data['password'])


@user_blueprint.route('/api/user', methods=["GET"])
def check_user_func():
    return user_checker()


@user_blueprint.route('/api/user', methods=["DELETE"])
def sign_out_func():
    return sign_out()


# 人際關係
# 從追蹤對象拿頭五篇reviews
@user_blueprint.route('/api/user/follows/reviews')
def get_latest_five_reviews_from_follows():
    return get_latest_five_reviews_from_follows_func()

# 看有沒有追蹤該頁面作者
@user_blueprint.route('/api/user_profile/<page_owner>')
def get_is_user_following(page_owner):
    print(page_owner)
    return get_is_user_following_func(page_owner)

# 追蹤
@user_blueprint.route('/api/user_profile/follows', methods=["PATCH"])
def follows_other_people():
    data = request.get_json()
    print('followers',data)
    following_name = data['following']
    follower = data['follower']
    return follows_other_people_func(following_name, follower)


# render watchlist
@user_blueprint.route('/user_profile/<page_master>/watchlist')
def render_user_watchlist_page(page_master):
    page_master = page_master.replace('+', ' ')

    return render_template('userWatchlist.html', pageMaster=page_master)


@user_blueprint.route('/api/user_profile/<page_master>/watchlist')
def get_watchlist_by_page(page_master):
    page_master = page_master.replace('+', ' ')
    page = request.args.get('page')
    print('view user get watchlist from ', page_master)

    return get_watchlist_by_page_func(page_master, page)


# 看該使用者有沒有把這電影加入watchlist/movies likes
@user_blueprint.route('/api/user_profile/user_movie_state', methods=["POST"])
def check_user_movie_state():
    try:
        data = request.get_json()
        print('check_movie_in_watch_list', data)
        movie_id = data['movieId']
        user_id = data['userId']
    except Exception as e:
        print('check_user_movie_state from user')
        print(e)
        return {'error': True}
    else:
        return check_user_movie_state_func(user_id, movie_id)


# 看該使用者有沒有把這review加入reviews likes 決定跟上面分開是因為film沒有review
@user_blueprint.route('/api/user_profile/user_review_state', methods=["POST"])
def user_review_state():
    try:
        data = request.get_json()
        print('check_review_in_review likes', data)
        review_id = data['reviewId']
        user_id = data['userId']
    except Exception as e:
        print('check_user_review likes from user')
        print(e)
        return {'error': True}
    else:
        return check_user_review_likes(user_id, review_id)


# 加入待看清單watchlist
@user_blueprint.route('/api/user_profile/watchlist', methods=["PATCH"])
def add_movie_to_watchlist():
    data = request.get_json()
    print('add to watchlist',data)
    movie_id = data['movieId']
    user_id = data['userId']
    return add_movie_to_watchlist_func(user_id, movie_id)


# delete watch list
@user_blueprint.route('/api/user_profile/watchlist', methods=["DELETE"])
def delete_movie_from_watchlist():
    data = request.get_json()
    print('delete from watchlist',data)
    movie_id = data['movieId']
    user_id = data['userId']
    return delete_movie_from_watchlist_func(user_id, movie_id)


# render likes
@user_blueprint.route('/user_profile/<page_master>/likes')
def render_user_likes_page(page_master):
    page_master = page_master.replace('+', ' ')
    print(page_master, 666666666)
    return render_template('userLikes.html', pageMaster=page_master)


# 加入likes_movies 喜歡這個電影
@user_blueprint.route('/api/user_profile/likes/movie', methods=["PATCH"])
def add_movie_to_likes():
    data = request.get_json()
    print('add to movie likes',data)
    movie_id = data['movieId']
    user_id = data['userId']
    return add_movie_to_likes_func(user_id, movie_id)


# delete movies user likes
@user_blueprint.route('/api/user_profile/likes/movie', methods=["DELETE"])
def delete_movie_from_likes():
    data = request.get_json()
    print('delete_movie_from_likes',data)
    movie_id = data['movieId']
    user_id = data['userId']
    return delete_movie_from_likes_func(user_id, movie_id)


# 拿多少人喜歡這reviews HERE
@user_blueprint.route('/api/user_profile/likes/review/<review_id>')
def get_total_review_likes(review_id):
    return get_total_review_likes_func(review_id)


# 加入likes_reviews 喜歡這個review
@user_blueprint.route('/api/user_profile/likes/review', methods=["PATCH"])
def add_review_to_likes():
    data = request.get_json()
    print('add to review likes', data)
    review_id = data['reviewId']
    user_id = data['userId']
    return add_review_to_likes_func(user_id, review_id)


# delete reviews user likes
@user_blueprint.route('/api/user_profile/likes/review', methods=["DELETE"])
def delete_review_from_likes():
    data = request.get_json()
    print('delete_movie_from_likes',data)
    review_id = data['reviewId']
    user_id = data['userId']
    return delete_review_from_likes_func(user_id, review_id)


# 拿追蹤的人最近喜歡了什麼評論 for index HERE
@user_blueprint.route('/api/<user_id>/get_following_latest_like_reviews/')
def get_following_latest_like_reviews(user_id):
    user_id = int(user_id)
    return get_following_latest_like_reviews_func(user_id)


# most popular reviews *4  for index HERE
@user_blueprint.route('/api/most_popular_reviews/')
def get_most_popular_reviews():
    return get_most_popular_reviews_func()


# user profile 上傳圖片
@user_blueprint.route('/api/user/<user_id>/upload_pic', methods=["PATCH"])
def upload_user_profile_pic(user_id):
    # data = request.get_json()
    # img = data['photoFile']
    img = request.files['photoFile']
    print(img)
    return upload_user_profile_pic_func(user_id, img)


# user profile 拿user上傳的照片 沒有就用預設
@user_blueprint.route('/api/user/<user_id>/upload_pic')
def get_user_profile_pic(user_id):
    return get_user_profile_pic_func(user_id)

