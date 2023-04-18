from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.hometown = data['hometown']
        self.profession = data['profession']
        self.education = data['education']
        self.favorite_dino = data['favorite_dino']
        self.about_user = data['about_user']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_discoveries = []

# login and registration
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, hometown, profession, education, favorite_dino, about_user, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(hometown)s, %(profession)s, %(education)s, %(favorite_dino)s, %(about_user)s, %(password)s);"
        return connectToMySQL('dinosaurdiscoveries').query_db(query, data)

    @classmethod
    def check_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('dinosaurdiscoveries').query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def check_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('dinosaurdiscoveries').query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('dinosaurdiscoveries').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
# validation for login and registration
    @staticmethod
    def validate_registration_form(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email =%(email)s;"
        results = connectToMySQL('dinosaurdiscoveries').query_db(query, user)
        if len(results) >= 1:
            flash("Email already taken!", 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Email is invalid.", 'register')
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First Name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['hometown']) < 2:
            flash("Hometown must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['profession']) < 2:
            flash("Profession must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['education']) < 2:
            flash("Please tell us your highest level of education. Minimum 2 characters", 'register')
            is_valid = False
        if len(user['favorite_dino']) < 2:
            flash("Please tell us your favorite dinosaur! Minimum 2 characters.", 'register')
            is_valid = False
        if len(user['about_user']) < 20:
            flash("Please tell us more about you! Must be at least 20 characters.", 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash("Password is invalid. Must be at least 8 characters.", 'register')
            is_valid = False
        if user['password'] != user['confirm_pw']:
            flash("Passwords do not match!!", 'register')
            is_valid = False
        return is_valid