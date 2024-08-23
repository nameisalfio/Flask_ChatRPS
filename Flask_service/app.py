from flask import Flask
import flask_mysqldb as mysqldb
from config import Config
from routes import main_bp  # Import the Blueprint

app = Flask(__name__)
app.config.from_object(Config)

mysql = mysqldb.MySQL(app)

# Register the Blueprint
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
