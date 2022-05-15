from models.movieData import *
from models.reviewData import *
import os

key = os.getenv('JWT_SECRET_KEY')

movie_database = MovieDatabase()
review_database = ReviewDatabase()


def get_user_latest_five_reviews_func(user_name):
    data = review_database.get_reviews_data(user_name)
    print(data)
    return {'ok':True}