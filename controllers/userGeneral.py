from models.userData import *

user_database = UserDatabase()


# check user movie state movielist/likes
def check_user_movie_state_func(user_id, movie_id):
    is_in_watchlist = user_database.check_user_state(user_id, movie_id, 'watchlist')
    is_in_movie_likes_list = user_database.check_user_state(user_id, movie_id, 'movieLikes')
    if is_in_watchlist is None:
        is_in_watchlist = False
    if is_in_movie_likes_list is None:
        is_in_movie_likes_list = False

    data = {
        'data': {
            'userWatchlist': is_in_watchlist,
            'userLikes': is_in_movie_likes_list
        }
    }
    return data


# 加入待看清單 watchlist
def add_movie_to_watchlist_func(user_id, movie_id):
    if user_id is None:
        return {'error': True,
                'message':'Please log in'}
    add_to_watchlist = user_database.add_to_watchlist(user_id, movie_id)
    if add_to_watchlist:
        return{'ok': True}
    else:
        return{'error': True,
               'message': 'Something went wrong, please try again'
               }


# delete from watchlist
def delete_movie_from_watchlist_func(user_id, movie_id):
    if user_id is None:
        return {'error': True,
                'message':'Please log in'}
    delete_from_watchlist = user_database.delete_from_watchlist(user_id, movie_id)
    if delete_from_watchlist:
        return {'ok': True}
    else:
        return {'error': True,
                'message': 'Something went wrong, please try again'
                }


def add_movie_to_likes_func(user_id, movie_id):
    if user_id is None:
        return {'error': True,
                'message':'Please log in'}
    movies_likes_added = user_database.add_to_movies_likes(user_id, movie_id)
    if movies_likes_added:
        return{'ok': True}
    else:
        return{'error': True,
               'message': 'Something went wrong, please try again'
               }


# delete from movies users likes
def delete_movie_from_likes_func(user_id, movie_id):
    if user_id is None:
        return {'error': True,
                'message': 'Please log in'}
    delete_from_movies_users_likes = user_database.delete_from_movies_users_likes(user_id, movie_id)
    if delete_from_movies_users_likes:
        return {'ok': True}
    else:
        return {'error': True,
                'message': 'Something went wrong, please try again'
                }