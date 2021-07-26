import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    MONGODB_SETTINGS = {
        'username': os.environ.get("MONGODB_BLOG_USERNAME"),
        'password': os.environ.get("MONGODB_BLOG_PASSWORD"),
        'host': os.environ.get("MONGODB_DATABASE_BLOG_URI")
    }