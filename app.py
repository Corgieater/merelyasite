from flask import *
import os
from dotenv import load_dotenv
from views.user import *
from views.search import *
from views.films import *
from views.userProfile import *


load_dotenv()
environment = os.getenv('FLASK_ENV')
flaskHost = os.getenv('FLASK_HOST')

app = Flask(
	__name__,
	static_folder='static',
	template_folder='templates'
)

app.register_blueprint(user_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(films_blueprint)
app.register_blueprint(user_profile_blueprint)


@app.route('/')
def index():
	return render_template('index.html')


if __name__ == '__main__' and environment == 'developmente':
	app.run(debug=True, host='localhost', port=3000)
else:
	app.run(host='0.0.0.0', port=3000)
