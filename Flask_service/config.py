import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '2a1a74c01e5d45133dfb10873cb31377')  # Flask secret key for CSRF protection
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Skills001!')
    MYSQL_DB = os.getenv('MYSQL_DB', 'ChatRPS')
    TEMP_FOLDER = os.getenv('TEMP_FOLDER', 'temp')  # Folder to save uploaded images temporarily
