from os import path


# Flask Settings
SECRET_KEY = 'secret_key'
IMAGE_UPLOADS = path.dirname(path.abspath(__file__)) + '/static/img_database'

# SQLAlchemy Settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../databases/login.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLite Settings
DATABASE = './databases/main_db.s3db'
