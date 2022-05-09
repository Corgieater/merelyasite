from flask import *
import jwt
from models.userData import *
from datetime import timedelta
import os

database = Database()
key = os.getenv('JWT_SECRET_KEY')

# 申請帳號相關功能
# 申請帳號
def sign_up(email, password, name):
    password = bcrypt.generate_password_hash(password)
    data = (None, name, email, password)
    email_duplication = database.get_email(email)

    # email重複就不用走下面流程了
    if email_duplication is True:
        return {
            'error': True,
            'message': 'Email already exist'
        }

    data_added = database.add_to_database(data)
    if data_added:
        return {
            'ok': True
        }
    else:
        return{
            'error': False
        }


# 登入相關
def log_in(email, password):
    # 先確認有沒有此email
    email_exist = database.get_email(email)
    if not email_exist:
        return {
            'error': True,
            'message': "This email doesn't exist"
        }

    user_info = database.check_user_log_in_info(email, password)
    if user_info:
        print(user_info)
        user_data = {
            'userName': user_info[0],
            'userEmail': user_info[1],
            'userId': user_info
        }

        encoded_data = jwt.encode(user_data, key, algorithm="HS256")
        res = make_response({'ok':True})
        res.set_cookie('user_info', encoded_data, timedelta(days=7))
        return res
    else:
        return{
            'error': True,
            'message': "Can't find user, please check your email or password again"
        }

# 檢查登入與否


def user_checker():
    try:
        token = request.cookies.get('user_info')
        if token is None:
            return {
                'data': None
            }
        data = jwt.decode(token, key, algorithms=["HS256"])
        print(data)
        if data:
            return {
                    'userName': data['userName']
                }

    except Exception as e:
        print(e)
        return {
            'data': None
        }


# 登出


def sign_out():
    res = make_response({'ok': True})
    res.set_cookie(key='user_info', value='', expires=0)
    print('out')
    return res

