from flask import Blueprint

from .auth_routes import auth_bp
from .user_routes import user_bp
from .rps_routes import rps_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(rps_bp, url_prefix='/rps')

