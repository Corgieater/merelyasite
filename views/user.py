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

# 追蹤
@user_blueprint.route('/api/user/follows/')
def follows_other_people():
    return follows_other_people_func()


