from flask import Blueprint
import requests
from controllers.auth import *
from controllers.social import *

user_blueprint = Blueprint(
    'user_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# 登入登出相關
@user_blueprint.route('/api/user', methods=['POST'])
def sign_up_func():
    data = request.get_json()
    return sign_up(data['email'], data['password'], data['name'])


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




