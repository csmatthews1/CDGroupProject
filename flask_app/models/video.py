from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, service

class Video:
    def __init__(self, data):
        self.id = data['id']
        self.category = data['category']
        self.title = data['title']
        self.img_url = data['img_url']
        self.info_url = data['info_url']
        self.type = data['type']
        self.rating = None
        self.service = None
       
    @classmethod
    def create_video(cls, data):
        query = 'INSERT INTO videos (category, title, img_url, info_url, type, created_at, updated_at, user_id, service_id) VALUE(%(category)s, %(title)s, %(img_url)s, %(info_url)s, %(type)s, NOW(), NOW(), %(user_id)s, %(service_id)s)'
        video = connectToMySQL('what_to_watch').query_db(query, data)
        return video

    @classmethod
    # this method will be used to for the "Recent Reviews" page
    def get_videos_with_recent_reviews(cls):
        query = 'SELECT * FROM videos JOIN reviews on videos.id = reviews.video_id ORDER BY reviews.created_at DESC LIMIT 4'
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
        query = 'SELECT * FROM videos JOIN users ON videos.user_id = user.id JOIN reviews ON videos.user_id = reviews.user_id WHERE videos.id = %(id)s'
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
            service_data ={
                'id' : row['service.id'],
                'name' : row['name'],
                'logo_url': row['logo_url'],
                'website' : row['website'],
                'created_at': row['service.created_at'],
                'updated_at': row['service.updated_at']
            }
            video = cls(row)
            video.rating = row['rating']
            video.service = service.Service(service_data)
            review_list.append(video)
        return review_list

    @classmethod
    def get_one(cls, data):
        query ='SELECT * FROM videos JOIN services ON videos.service_id = service.id WHERE videos.id = %(id)s'
        video = connectToMySQL('watch_to_watch').query_db(query, data)
        result = cls(video[0])
        service_data = {
            'id' : video[0]['service.id'],
            'name' : video[0]['name'],
            'logo_url': video[0]['logo_url'],
            'website' : video[0]['website'],
            'created_at': video[0]['service.created_at'],
            'updated_at': video[0]['service.updated_at']
        }
        result.service = service.Service(service_data)
        return result
