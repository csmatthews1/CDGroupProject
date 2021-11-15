from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, video

class Service:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.logo_url = data['logo_url']
        self.website = data['website']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_service(cls, data):
        query = 'INSERT INTO services (name, logo_url, website, created_at, updated_at) VALUE(%(name)s, %(logo_url)s, %(website)s, NOW(), NOW()) '
        service = connectToMySQL('what_to_watch').query_db(query, data)
        return service