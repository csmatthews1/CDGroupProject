from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, service, review

class Video:
    def __init__(self, data):
        self.id = data['id']
        self.category = data['category']
        self.title = data['title']
        self.img_url = data['img_url']
        self.info_url = data['info_url']
        self.type = data['type']
        self.reviews = []
        self.service = None
        self.avg_rating = 0.0;
       
    @classmethod
    def create_video(cls, data):
        query = 'INSERT INTO videos (category, title, img_url, info_url, type, created_at, updated_at, user_id, service_id) VALUE(%(category)s, %(title)s, %(img_url)s, %(info_url)s, %(type)s, NOW(), NOW(), %(user_id)s, %(service_id)s)'
        video = connectToMySQL('what_to_watch').query_db(query, data)
        return video

    @classmethod
    # this method will be used to for the "Recent Reviews" page
    def get_videos_with_recent_reviews(cls):
        query = 'SELECT * FROM videos ORDER BY videos.created_at DESC LIMIT 4'
        results = connectToMySQL('what_to_watch').query_db(query)
        video_list = []
        for row in results:
            video = cls(row)
            data = {
                'id': video.id
            }
            # Get all reviews for each video
            query = 'SELECT * FROM reviews WHERE video_id = %(id)s'
            results = connectToMySQL('what_to_watch').query_db(query, data)
            for r in results:
                video.reviews.append(review.Review(r))

            #calculate average rating for each video
            for r in video.reviews:
                video.avg_rating += float(r.rating)
            video.avg_rating /= len(video.reviews)

            # Get service object for each video
            service_data ={
                'id' : row['service_id'],
            }
            video.service = service.Service.get_by_id(service_data)
            video_list.append(video)
        return video_list

    @classmethod
    # this method is for "All Reviews" page
    def get_all_reviews(cls):
        query = 'SELECT * FROM videos ORDER BY videos.created_at DESC'
        results = connectToMySQL('what_to_watch').query_db(query)
        review_list = []
        for row in results:
            video = cls(row)
            data = {
                'id': video.id
            }
            # Get all reviews for each video
            query = 'SELECT * FROM reviews WHERE video_id = %(id)s'
            results = connectToMySQL('what_to_watch').query_db(query, data)
            for r in results:
                video.reviews.append(review.Review(r))

            #calculate average rating for each video
            for r in video.reviews:
                video.avg_rating += float(r.rating)
            video.avg_rating /= len(video.reviews)

            # Get service object for each video
            service_data ={
                'id' : row['service_id'],
            }
            video.service = service.Service.get_by_id(service_data)
            review_list.append(video)

        return review_list

    @classmethod
    def get_by_id(cls, data):
        query ='SELECT * FROM videos WHERE videos.id = %(id)s'
        video = connectToMySQL('what_to_watch').query_db(query, data)
        result = cls(video[0])
        
        data = {
            'id': result.id
        }
        # Get all reviews for each video
        query = 'SELECT * FROM reviews WHERE video_id = %(id)s'
        results = connectToMySQL('what_to_watch').query_db(query, data)
        for r in results:
            result.reviews.append(review.Review(r))

        #calculate average rating for this video
        for r in result.reviews:
            result.avg_rating += float(r.rating)
        result.avg_rating /= len(result.reviews)

        #Get service object for this video
        service_data = {
            'id' : video[0]['service_id']
        }
        result.service = service.Service.get_by_id(service_data)
        return result
