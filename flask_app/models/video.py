from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Video:
    def __init__(self, data):
        self.id = data['id']
        self.category = data['category']
        self.title = data['title']
        self.img_url = data['img_url']
        self.info_url = data['info_url']
        self.type = data['type']
        self.rating = None
        self.service_name = None
       
    @classmethod
    def create_video(cls, data):
        query = 'INSERT INTO videos (category, title, img_url, info_url, type, created_at, updated_at, user_id, service_id) VALUE(%(category)s, %(title)s, %(img_url)s, %(info_url)s, %(type)s, NOW(), NOW(), %(user_id)s, %(service_id)s)'
        video = connectToMySQL('what_to_watch').query_db(query, data)
        return video

    @classmethod
    # this method will be used to for the "Recent Reviews" page
    def get_videos_with_recent_reviews(cls):
        query = 'SELECT * FROM videos JOIN reviews ON videos.id = reviews.video_id ORDER BY reviews.created_at DESC LIMIT 4'
        results = connectToMySQL('what_to_watch').query_db(query)
        video_list = []
        for row in results:
            video = cls(row)
            video.rating = row['rating']
            video_list.append(video)
        return video_list

    @classmethod
    # this method is to display the video and the creators rating above the "User Reviews" heading
    def get_video_with_creator_rating(cls, data):
        query = 'SELECT * FROM videos JOIN users ON videos.user_id = users.id JOIN reviews ON videos.user_id = reviews.user_id WHERE videos.id = %(id)s'
        result = connectToMySQL('what_to_watch').query_db(query, data)
        video = cls(result[0])
        video.rating = result[0]['rating']
        return video

    @classmethod
    # this method is for "All Reviews" page
    def get_all_reviews(cls):
        query = 'SELECT * FROM videos JOIN reviews ON videos.id = review.video_id JOIN services on videos.service_id = service.id ORDER BY review.created_at DESC'
        results = connectToMySQL('what_to_watch').query_db(query)
        review_list = []
        for row in results:
            video = cls(row)
            video.rating = row['rating']
            video.service_name = row['name']
            review_list.append(video)
        return review_list

    @classmethod
    def get_one(cls, data):
        query ='SELECT * FROM videos JOIN services ON videos.service_id = service.id WHERE videos.id = %(id)s'
        video = connectToMySQL('watch_to_watch').query_db(query, data)
        result = cls(video[0])
        result.service_name = video[0]['name']
        return result
