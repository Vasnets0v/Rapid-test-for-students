from os import path


# Flask Settings
SECRET_KEY = 'secret_key'
IMAGE_UPLOADS = path.dirname(path.abspath(__file__)) + '/static/img_database'

# SQLAlchemy Settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/admin.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SQLite Settings
DATABASE = '../database/main_db.s3db'
