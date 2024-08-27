from app import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name, lastname, username, email, password):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.username}>'
