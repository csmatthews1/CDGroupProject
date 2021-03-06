from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, video,service

class Review:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.video_id = data['video_id']
        self.rating = data['rating']
        self.comments = data['comments']


    @classmethod
    def create_review(cls, data):
        query = 'INSERT INTO reviews (user_id, video_id, rating, comments, created_at, updated_at) VALUES (%(user_id)s, %(video_id)s, %(rating)s, %(comments)s, NOW(), NOW())'
        review = connectToMySQL('what_to_watch').query_db(query, data)
        return review
    @classmethod
    # this method is to display all the reviews under the "User Reviews" heading
    def get_all_reviews_for_video(cls, data):
        query = 'SELECT * FROM reviews JOIN videos ON reviews.video_id = video.id WHERE videos.id = %(id)s'
        results = connectToMySQL('what_to_watch').query_db(query, data)
        reviews = []
        for row in results:
            review = cls(row)
            reviews.append(review)
        return reviews