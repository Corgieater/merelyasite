import requests
from dotenv import load_dotenv
from urllib.request import urlopen
import json
from os.path import basename
import boto3
import os
from models.addMovieToData import ImportDatabase
load_dotenv()

key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
omdb_key = os.getenv('TMDB_KEY')

client = boto3.client('s3',
                      aws_access_key_id=key_id,
                      aws_secret_access_key=secret_key
                      )


def get_movie_from_omdb_func(title, year):
    database = ImportDatabase()
    title = title.replace(' ', '+')
    url = f'http://www.omdbapi.com/?apikey={omdb_key}&t={title}&y={year}&plot=full'
    data_exist = database.find_in_database(title, year)
    if data_exist:
        return False
    else:
        movie_id = database.check_last_movie_id()[0]+1
        response = urlopen(url)
        data = json.loads(response.read())
        title = data['Title']
        year = data['Year']
        genre = data['Genre']
        director = data['Director']
        actors = data['Actors']
        story_line = data['Plot']
        tagline
        poster = data['Poster']
        cut_point = poster.find('_S')
        # 換成大張的海報
        poster = poster[:cut_point] + '_FMjpg_UX674_.jpg'
        print(movie_id, title, year, genre, director, actors, story_line, poster)
        movie_input = (movie_id, movie_id,title, year, story_line, tagline)
        print(movie_input)
        try:
            database.add_to_database(movie_input)
            # 丟S3
            with open(basename(poster), 'wb') as f:
                client.put_object(
                    Bucket='merelyasite-bucket',
                    Body=requests.get(poster).content,
                    Key=f'posters/img{movie_id}.jpg',
                    ContentType='image/jpeg',
                )
        except Exception as e:
            print(e)
            return False
        else:
            return True
