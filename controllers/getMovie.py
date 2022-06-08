import requests
from os.path import basename
import boto3
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from imdb import Cinemagoer
from models.addMovieToData import *

load_dotenv()

key_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('BUCKET_NAME')


client = boto3.client('s3',
                      aws_access_key_id=key_id,
                      aws_secret_access_key=secret_key
                      )

user_agent = UserAgent()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/"
              "webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.8",
    "Host": "www.imdb.com",  #目標網站
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": user_agent.random,
    "Referer": "https://www.google.com/"
}

imdb_move_base = Cinemagoer()
add_movie_database = ImportDatabase()

global genre_count
genre_count = 0


def get_imdb_id(title, year):
    print(title, year)
    movies = imdb_move_base.search_movie(title)
    print(movies)
    imdb_movie_id = None
    for movie in movies:
        print(666,movie['title'], movie['year'])
        try:
            if movie['title'].lower() == title.lower() \
                    and movie['year'] == int(year) and movie['kind'] == 'movie':
                imdb_movie_id = movie.movieID
                break
        except Exception as e:
            print('something wrong on get movie from imdb')
            print(e)
    return imdb_movie_id


def cut_string(string, target):
    target_index = string.index(target)
    result = string[:target_index]
    return result


def clean_by_input(soup, input_text):
    item_list = []
    for item in soup.find(text=input_text).findNext('div').findNext('ul').findAll('li'):
        result = item.find('a').getText()
        item_list.append(result)
    return item_list


def random_delay(time_list):
    delay_choices = time_list
    delay = random.choice(delay_choices)
    time.sleep(delay)

# poster to s3
def up_load_to_s3(poster_url, movie_id):
    # 丟S3
    with open(basename(poster_url), 'wb') as f:
        client.put_object(
            Bucket=bucket_name,
            Body=requests.get(poster_url).content,
            Key=f'moviePos/img{movie_id}.jpg',
            ContentType='image/jpeg',
        )

def get_movie_from_imdb_func(title, year):
    global genre_count
    is_movie_in_database = add_movie_database.find_in_database(title, year)
    poster_url = None
    if is_movie_in_database:
        return{'error': True,
               'message': 'Movie already exist'}
    else:
        imdb_movie_id = None
        try:
            imdb_movie_id = get_imdb_id(title, year)
            print('imdb_movie_id', imdb_movie_id)
        except Exception as e:
            print('something went wrong on imdb database')
            print(e)
            return {
            'error': True,
            'message': 'Something is wrong, please check the title and year'
            }
        url = f'https://www.imdb.com/title/tt{imdb_movie_id}/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=1a264172-ae1142e4-' \
              f'8ef7-7fed1973bb8f&pf_rd_r=STTXPSSSH1CW5RG8QKKM&pf_rd_s=center-1&pf_rd_t=15506&pf_rd_i' \
              f'=top&ref_=chttp_tt_3'
        if imdb_movie_id == None:
            return {'error':True,
                    'message':"Sorry, we can't find this movie, please check again"}
        print(url)
        try:
            page = requests.get(url, headers=headers)
        except Exception as e:
            print('something wrong when doing request page to imdb, maybe user is trolling')
            print(e)
            return {
                'error': True,
                'message': 'Something is wrong, please check the title and year'
            }
        soup = BeautifulSoup(page.text, 'html.parser')
        scraped_movie = []

        unclean_title = None
        unclean_year = None
        try:
            unclean_title = soup.title.string
        except Exception as e:
            print(e)

        try:
            unclean_year = soup.findAll \
                ('a', class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh")
        except Exception as e:
            print(e)

        # 判斷是否有多個genre/director genre out
        # find_genre = soup.find(text='Genre')
        find_director = soup.find(text='Director')

        m_title = cut_string(unclean_title, ' (')
        scraped_movie.append(m_title)
        year = unclean_year[0].string
        scraped_movie.append(year)
        try:
            story_line = soup.find('span', class_='sc-16ede01-2 gXUyNh').getText()
            scraped_movie.append(story_line)
        except Exception as e:
            print(e)
        try:
            find_tag_line = soup.find(text="Taglines")
            tag_line = find_tag_line.findNext('div').findNext('ul') \
                .findNext('li').findNext('span').getText()
            scraped_movie.append(tag_line)
        except Exception as e:
            scraped_movie.append('')
            print(e)
        genres = []
        directors = []
        actors = []

        # this is more reliable
        genres_list = soup.findAll('li', class_="ipc-inline-list__item ipc-chip__text",
                                   attrs={'role': 'presentation'})
        print(genre_count, '\ngenre_count')
        for g in genres_list:
            if genre_count < 3:
                print(genre_count, '\ngenre_count')
                genre = g.get_text()
                genres.append(genre.title())
                genre_count += 1

        try:
            actors = soup.find(text='Stars')
            actors = clean_by_input(soup, 'Stars')
        except Exception as e:
            print(e)

        # dealing with directors
        if find_director is None:
            directors = clean_by_input(soup, 'Directors')
        else:
            directors.append(soup.find(text='Director').findNext('div').findNext('ul').
                             find('li').find('a').getText())

        # get poster url
        try:
            imdb_poster_url = 'https://www.imdb.com' + \
                              soup.find('a', attrs={'class': 'ipc-lockup-overlay ipc-focusable'})['href']
            random_delay([5, 3, 4, 6, 10, 11])
            poster_place = requests.get(imdb_poster_url, headers=headers)
            soup = BeautifulSoup(poster_place.text, 'html.parser')
            poster_url = soup.find('img', attrs={'class': 'sc-7c0a9e7c-0 hXPlvk'})['src']
            try:
                print('poster here', poster_url)
            except Exception as e:
                print(e)

        except Exception as e:
            print(e, 'skip')

        added_movie_id = add_movie_database.add_to_database(scraped_movie, directors, actors, genres)
        if added_movie_id:
            for director in directors:
                director_id = add_movie_database.find_input_from_table('director_id', 'directors', 'name', director)
                if director_id is not None:
                    add_movie_database.add_relationship((director_id, added_movie_id),'director')
                else:
                    new_director_id = add_movie_database.add_subject_to_database_by_type(director, 'director')[0]
                    add_movie_database.add_relationship((new_director_id, added_movie_id), 'director')

            for actor in actors:
                actor_id = add_movie_database.find_input_from_table('actor_id', 'actors', 'name', actor)
                if actor_id is not None:
                    add_movie_database.add_relationship((actor_id, added_movie_id), 'actor')
                else:
                    new_actor_id = add_movie_database.add_subject_to_database_by_type(actor, 'actor')[0]
                    add_movie_database.add_relationship((new_actor_id, added_movie_id), 'actor')

            for genre in genres:
                genre_id = add_movie_database.find_input_from_table('genre_id', 'genres', 'type', genre)
                if genre_id is not None:
                    add_movie_database.add_relationship((genre_id, added_movie_id), 'genre')
                else:
                    new_genre_id = add_movie_database.add_subject_to_database_by_type(genre, 'genre')[0]
                    add_movie_database.add_relationship((new_genre_id, added_movie_id), 'genre')

            genre_count = 0

            try:
                up_load_to_s3(poster_url, added_movie_id)
            except Exception as e:
                print('up load to s3 got trouble')
                print(e)
                return {'error': True,
                        'message': "There is no poster"}
            else:
                return{'ok': True}
