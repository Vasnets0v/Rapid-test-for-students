import os
import sqlite3
import time
import argparse
from werkzeug.security import generate_password_hash

parser = argparse.ArgumentParser()

parser.add_argument('email', help="email of the first admin (the database cannot contain the same emails)")
parser.add_argument('name', help="name of admin")
parser.add_argument('surname', help="surname of admin")
parser.add_argument('password', help="password")

args = parser.parse_args()


def create_directories():
    if os.path.exists("database"):
        pass
    else:
        os.mkdir("database")

    if os.path.exists("application/static/img_database"):
        pass
    else:
        os.mkdir("application/static/img_database")


def create_db_and_base_table():
    with sqlite3.connect('database/main_db.s3db', check_same_thread=False) as db:
        sql_request = db.cursor()

        sql_request.execute(f"""
        CREATE TABLE IF NOT EXISTS setting (
        id integer PRIMARY KEY AUTOINCREMENT,
        topic_title varchar(64),
        time_to_pass integer,
        topic_status varchar(64),
        questions integer,
        priority integer
        );""")

        db.commit()


def create_first_admin():
    with sqlite3.connect('database/admin.db', check_same_thread=False) as db:
        sql_request = db.cursor()

        first_admin = "INSERT INTO user (email, name, surname, password, time_of_creation) VALUES (?, ?, ?, ?, ?)"
        admin_data = (args.email, args.name, args.surname, generate_password_hash(args.password) ,time.strftime("%d.%m.%Y %H:%M"))
        sql_request.execute(first_admin, admin_data)

        db.commit()


create_directories()
create_db_and_base_table()
create_first_admin()
