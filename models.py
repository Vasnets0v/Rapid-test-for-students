from flask_login import UserMixin
from app import db_alchemy, sql_request


class User(UserMixin, db_alchemy.Model):
    id = db_alchemy.Column(db_alchemy.Integer, primary_key=True)
    email = db_alchemy.Column(db_alchemy.String(64), unique=True, nullable=False)
    name = db_alchemy.Column(db_alchemy.String(16), nullable=False)
    surname = db_alchemy.Column(db_alchemy.String(16), nullable=False)
    password = db_alchemy.Column(db_alchemy.String(512), nullable=False)
    time_of_creation = db_alchemy.Column(db_alchemy.String(64), nullable=False)


def table_for_new_topic(new_topic):
    sql_request.execute(f"""
    CREATE TABLE IF NOT EXISTS {new_topic} (
        id integer PRIMARY KEY AUTOINCREMENT,
        question varchar(255),
        img_question varchar(255),
        answer_1 varchar(255),
        answer_2 varchar(255),
        answer_3 varchar(255),
        answer_4 varchar(255),
        answer_5 varchar(255),
        answer_6 varchar(255),
        img_1 varchar(255),
        img_2 varchar(255),
        img_3 varchar(255),
        img_4 varchar(255),
        img_5 varchar(255),
        img_6 varchar(255),
        right_answer varchar(255)
        );""")


def student_score(topic):
    sql_request.execute(f"""
    CREATE TABLE IF NOT EXISTS score_for_theme_{topic} (
    id integer PRIMARY KEY AUTOINCREMENT,
    user_name varchar(64),
    user_group varchar(16),
    percentage_score integer,
    end_time varchar(16)
    );""")


# information about all exists tests
def tests_info():
    sql_request.execute(f"""
    CREATE TABLE IF NOT EXISTS tests_info (
    id integer PRIMARY KEY AUTOINCREMENT,
    topic_title varchar(64),
    time_to_pass integer,
    topic_status varchar(64),
    questions integer
    );""")
