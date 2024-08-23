from .main import main_bp
from .users import users_bp
from .conversations import conversations_bp
from .upload_image import upload_image_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(conversations_bp)
    app.register_blueprint(upload_image_bp)
