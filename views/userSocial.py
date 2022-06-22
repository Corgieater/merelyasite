from controllers.social import *
user_social_blueprint = Blueprint(
    'user_social_blueprint',
    __name__,
    static_folder='static',
    template_folder='templates'
)


# 人際關係
# 從追蹤對象拿頭五篇reviews
@user_social_blueprint.route('/api/user/following/reviews')
def get_latest_five_reviews_from_follows():
    return get_latest_five_reviews_from_follows_func()


# 看有沒有追蹤該頁面作者
@user_social_blueprint.route('/api/user_profile/<page_owner>')
def get_is_user_following(page_owner):
    return get_is_user_following_func(page_owner)


# 追蹤
@user_social_blueprint.route('/api/user_profile/follows', methods=["PATCH"])
def follows_other_people():
    data = request.get_json()
    following_name = data['following']
    follower = data['follower']
    return follows_other_people_func(following_name, follower)


# 拿追蹤的人最近喜歡了什麼評論給index用
@user_social_blueprint.route('/api/<user_id>/following_latest_like_reviews/')
def get_following_latest_like_reviews(user_id):
    user_id = int(user_id)
    return get_following_latest_like_reviews_func(user_id)


# 拿多少人喜歡這reviews
@user_social_blueprint.route('/api/user_profile/likes/review/<review_id>')
def get_total_review_likes(review_id):
    return get_total_review_likes_func(review_id)


# 加入likes_reviews 喜歡這個review
@user_social_blueprint.route('/api/user_profile/likes/review', methods=["PATCH"])
def add_review_to_likes():
    data = request.get_json()
    review_id = data['reviewId']
    user_id = data['userId']
    return add_review_to_likes_func(user_id, review_id)


# delete reviews user likes
@user_social_blueprint.route('/api/user_profile/likes/review', methods=["DELETE"])
def delete_review_from_likes():
    data = request.get_json()
    review_id = data['reviewId']
    user_id = data['userId']
    return delete_review_from_likes_func(user_id, review_id)


# most popular reviews *4 給index用
@user_social_blueprint.route('/api/most_popular_reviews/')
def get_most_popular_reviews():
    return get_most_popular_reviews_func()
