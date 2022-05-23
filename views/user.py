from flask import Blueprint
import requests
from controllers.auth import *

user_blueprint = Blueprint(
    'user_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@user_blueprint.route('/api/user', methods=['POST'])
def sign_up_func():
    data = request.get_json()
    print(data)
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
