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

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM services WHERE id = %(id)s'
        service = connectToMySQL('what_to_watch').query_db(query, data)
        if len(service) < 1:
            return False
        return cls(service[0])    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM services;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('what_to_watch').query_db(query)
        # Create an empty list to append our instances of friends
        services = []
        # Iterate over the db results and create instances of friends with cls.
        for service in results:
            services.append( cls(service) )
        return services