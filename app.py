from flask import *
import os

environment = os.getenv('FLASK_ENV')
flaskHost = os.getenv('FLASK_HOST')


app = Flask(
	__name__,
	static_folder='static',
	template_folder='templates'
)


@app.route('/')
def index():
	return render_template("index.html")


if __name__ == '__main__' and environment == 'developmente':
	app.run(debug=True, port=3000)
else:
	app.run(host=flaskHost, port=3000)
