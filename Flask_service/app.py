from flask import Flask
import flask_mysqldb as mysqldb
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = mysqldb.MySQL(app)

# Importa le rotte dopo aver inizializzato l'app e MySQL
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
