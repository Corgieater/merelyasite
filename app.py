from views.user import *
from views.search import *
from views.films import *
from views.userProfile import *
from views.userSocial import *
from views.reviewsAndRates import *

load_dotenv()
environment = os.getenv('FLASK_ENV')
auth_email_password = os.getenv('AUTH_EMAIL_PASSWORD')
flash_secret_key = os.getenv('SECRET_KEY_FOR_FLASH')


app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

app.secret_key = flash_secret_key

app.register_blueprint(user_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(films_blueprint)
app.register_blueprint(user_profile_blueprint)
app.register_blueprint(user_social_blueprint)
app.register_blueprint(reviewsAndRates_blueprint)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__' and environment == 'development':
    app.run(debug=True, host='localhost', port=3000, use_reloader=False)
else:
    app.run(host='0.0.0.0', port=3000)
