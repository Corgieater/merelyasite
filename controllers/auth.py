from flask import *
import jwt
from models.userData import *
from datetime import timedelta
import os
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message

key = os.getenv('JWT_SECRET_KEY')
auth_secret_key = os.getenv('EMAIL_AUTH_SECRET_KEY')
salt_secret_key = os.getenv('SALT_SECRET_KEY')
auth_email_password = os.getenv('AUTH_EMAIL_PASSWORD')
flask_env = os.getenv('FLASK_ENV')


app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PROT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='merelyasite@gmail.com',
    MAIL_PASSWORD=auth_email_password
)

mail = Mail(app)

# 申請帳號相關功能
# 申請帳號
database = UserDatabase()


# check is name taken
def check_user_name_func(sign_up_name):
    user_name_exist = database.check_user_name(sign_up_name)
    if user_name_exist:
        return{'error': True}
    else:
        return{'ok': True}


def sign_up(email, password, name):
    password = bcrypt.generate_password_hash(password)
    data = (None, name, email, password)
    # 檢查email是否重複
    email_duplication = database.get_email(email)
    # 用email產生驗證碼
    auth_code = create_auth_code(email)
    print(auth_code)
    # 寄信
    send_email(email, name)
    # email重複就不用走下面流程了
    if email_duplication is True:
        return {
            'error': True,
            'message': 'Email already exist'
        }

    last_insert_user_id = database.add_to_database(data)
    print('last_insert_user_id looks like this',last_insert_user_id)

    if last_insert_user_id:
        user_data = {
            'userName': name,
            'userId': last_insert_user_id[0]
        }

        encoded_data = jwt.encode(user_data, key, algorithm="HS256")
        res = make_response({'ok': True})
        res.set_cookie('user_info', encoded_data, timedelta(days=7))
        return res
        # return {
        #     'ok': True
        # }
    else:
        return{
            'error': False
        }


# 把email包成auth code
def create_auth_code(email):
    serializer = URLSafeTimedSerializer(auth_secret_key)
    token = serializer.dumps(email, salt=salt_secret_key)
    return token


def send_email(email, name, token=None):
    with app.app_context():
        token = create_auth_code('cekada9453@jrvps.com')

        msg_sender = 'merelyasite@gmail.com'
        msg_recipients = [email]
        msg_title = 'Please validate your Movie Notes account'
        if flask_env == 'development':
            action_url = f'http://localhost:3000/api/user/validation/{token}'
        else:
            action_url = f'https://merelyasite.xyz/api/user/validation/{token}'
        msg_html = f'''<p>Welcome!, {name} Please validate your email address by clicking this button.
    The link remains valid for 48 hours.</p> <br> <form action="{action_url}">
        <input type="submit" value="Validate your account" />
    </form>'''
        msg = Message(msg_title, sender=msg_sender, recipients=msg_recipients)
        msg.html = msg_html
        mail.send(msg)

# OMG THIS WORKED???
# send_email('cekada9453@jrvps.com', 'jojo')


# 確認使用者
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(auth_secret_key)
    try:
        email = serializer.loads(token, salt=salt_secret_key, max_age=expiration)
    except:
        return False
    else:
        print(email)
        database.renew_email_confirm(email)
        return True


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
        user_data = {
            'userName': user_info[0],
            'userId': user_info[1]
        }

        encoded_data = jwt.encode(user_data, key, algorithm="HS256")
        res = make_response({'ok': True})
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
        if data:
            return {
                    'userName': data['userName'],
                    'userId': data['userId']
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
    return res

