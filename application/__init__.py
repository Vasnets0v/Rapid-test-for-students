from flask import Flask, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from config import DATABASE

# Create an application and login manager
app = Flask(__name__)
login_manager = LoginManager(app)

# Load App Settings
app.config.from_pyfile('config.py')

db_alchemy = SQLAlchemy(app)

# Create a SQLite database connection when needed
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

from routes import *


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1194)
    