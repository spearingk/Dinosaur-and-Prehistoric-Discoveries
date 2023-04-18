from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Discovery:
    def __init__(self, data):
        self.id = data['id']
        self.discovery_name = data['discovery_name']
        self.discovery_location = data['discovery_location']
        self.discovery_date = data['discovery_date']
        self.discovery_details = data['discovery_details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.users_who_favorited = []

# Validations
    @staticmethod
    def validate_discovery_form(data):
        is_valid = True
        if len(data['discovery_name']) <= 0:
            flash("Name of discovery is required!", 'discovery')
            is_valid = False
        if len(data['discovery_location']) <= 0:
            flash("Location of discovery is required!", 'discovery')
            is_valid = False
        if len(data['discovery_date']) <= 0:
            flash("Discovery date is required!", 'discovery')
            is_valid = False
        if len(data['discovery_details']) <= 20:
            flash("Details of the discovery are required! Please provide as many details as possible.", 'discovery')
            is_valid = False
        return is_valid

# get all discoveries
    @classmethod
    def get_all(cls, data):
        query = """
                SELECT * FROM discoveries 
                JOIN users ON discoveries.user_id = users.id;
                """
        results = connectToMySQL('dinosaurdiscoveries').query_db(query, data)
        discoveries = []
        for discovery in results:
            this_discovery = cls(discovery)
            user_data = {
                    'id': discovery['users.id'],
                    'first_name': discovery['first_name'],
                    'last_name': discovery['last_name'],
                    'email': discovery['email'],
                    'hometown': discovery['hometown'],
                    'profession': discovery['profession'],
                    'education': discovery['education'],
                    'favorite_dino': discovery['favorite_dino'],
                    'about_user': discovery['about_user'],
                    'password': discovery['password'],
                    'created_at': discovery['users.created_at'],
                    'updated_at': discovery['users.updated_at']
                }
            this_discovery.user = user.User(user_data)
            discoveries.append(this_discovery)
        return discoveries
    
# get one discovery by id
    @classmethod
    def get_one_by_id(cls, data):
        query = """
                SELECT * FROM discoveries 
                JOIN users ON discoveries.user_id = users.id 
                WHERE discoveries.id = %(id)s;
                """
        result = connectToMySQL('dinosaurdiscoveries').query_db(query, data)
        if not result:
            return False
        result = result[0]
        this_discovery = cls(result)
        user_data = {
                'id': result['user_id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'hometown': result['hometown'],
                'profession': result['profession'],
                'education': result['education'],
                'favorite_dino': result['favorite_dino'],
                'about_user': result['about_user'],
                'password': result['password'],
                'created_at': result['users.created_at'],
                'updated_at': result['users.updated_at']
            }
        this_discovery.user = user.User(user_data)
        return this_discovery

# create discovery
    @classmethod
    def create_discovery(cls, data):
        if not cls.validate_discovery_form(data):
            return False
        
        query = """
                INSERT INTO discoveries (discovery_name, discovery_location, discovery_date, discovery_details, user_id) 
                VALUES (%(discovery_name)s, %(discovery_location)s, %(discovery_date)s, %(discovery_details)s, %(user_id)s);
                """
        return connectToMySQL('dinosaurdiscoveries').query_db(query, data)

# edit discovery
    @classmethod
    def edit_discovery(cls, data):
        if not cls.validate_discovery_form(data):
            return False

        query = """
                UPDATE discoveries 
                SET discovery_name=%(discovery_name)s, 
                discovery_location=%(discovery_location)s, 
                discovery_date=%(discovery_date)s, 
                discovery_details=%(discovery_details)s 
                WHERE discoveries.id=%(id)s;
                """
        return connectToMySQL('dinosaurdiscoveries').query_db(query, data)

# delete discovery
    @classmethod
    def delete_discovery(cls, data):
        query = "DELETE FROM discoveries WHERE id = %(id)s;"
        return connectToMySQL('dinosaurdiscoveries').query_db(query, data)