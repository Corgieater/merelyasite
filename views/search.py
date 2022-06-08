from controllers.search import *

from flask import *

search_blueprint = Blueprint(
    'search_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)

# http://localhost:3000/search?keyword=&page=1
# 網頁右上角的搜尋from OK
@search_blueprint.route('/api/search')
def search():
    user_keyword = request.args.get('keyword')
    user_page = request.args.get('page')
    print(user_keyword)
    print(user_page)
    return get_info_func(user_keyword, user_page)


@search_blueprint.route('/search')
def render_search_page():
    movie = request.args.get('keyword').replace('+', ' ')
    return render_template('searchResults.html', movie=movie)


# 找導演
@search_blueprint.route('/api/search/director')
def get_director():
    director = request.args.get('director').replace('+', ' ')
    page = request.args.get('page')
    if page is None:
        page = 1
    return get_data_by_type_func(director, page, 'director')


# 找導演page render(有可愛logo那個)
@search_blueprint.route('/search/director')
def render_search_director_page():
    director = request.args.get('director').replace('+', ' ')
    return render_template('searchDirector.html', director=director)


# 找演員
@search_blueprint.route('/api/search/actor')
def get_actor():
    actor = request.args.get('actor').replace('+', ' ')
    page = request.args.get('page')
    if page is None:
        page = 1
    return get_data_by_type_func(actor, page, 'actor')


# 找演員 page render(有可愛logo那個)
@search_blueprint.route('/search/actor')
def render_search_actor_page():
    actor = request.args.get('actor').replace('+', ' ')
    return render_template('searchActor.html', actor=actor)

# genre 找電影+director
@search_blueprint.route('/api/search/genre')
def search_by_genre():
    genre = request.args.get('genre')
    page = request.args.get('page')
    print('genre', genre, page)
    return get_films_by_genre_func(genre, page)


# render template genre
@search_blueprint.route('/search/genre')
def render_search_genre_page():
    genre = request.args.get('genre').replace('+', ' ')
    return render_template('searchGenre.html', genre=genre)


# 用user name找user
@search_blueprint.route('/api/search/users')
def get_users_by_name():
    user = request.args.get('user')
    page = request.args.get('page')
    return get_users_by_name_func(user, page)


# render template search users
@search_blueprint.route('/search/users')
def render_search_users_page():
    user = request.args.get('user').replace('+', ' ')
    return render_template('searchUsers.html', user=user)


# 電影title或心得內容找review
@search_blueprint.route('/api/search/reviews')
def get_reviews_from_title_or_content():
    review_query = request.args.get('reviews').replace('+', ' ')
    page = request.args.get('page')
    print('reviews', review_query, page)
    return get_reviews_from_title_or_content_func(review_query, page)


# render template search reviews
@search_blueprint.route('/search/reviews')
def render_search_reviews_page():
    review_query = request.args.get('reviews').replace('+', ' ')
    print('render_search_reviews_page', review_query)
    return render_template('searchReviews.html', reviews=review_query)
