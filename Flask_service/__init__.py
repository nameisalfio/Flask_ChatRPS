from flask import Flask
from flask_mysqldb import MySQL
from .config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MySQL connection
    mysql.init_app(app)
    
    # Register blueprints
    from .routes import register_blueprints
    register_blueprints(app)

    return app
