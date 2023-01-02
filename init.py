import os
import sqlite3

def create_directories():
    if os.path.exists("databases"):
        pass
    else:
        os.mkdir("databases")

    if os.path.exists("static/img_database"):
        pass
    else:
        os.mkdir("static/img_database")


def create_db_and_base_table():
    db = sqlite3.connect('databases/main_db.s3db', check_same_thread=False)
    sql_request = db.cursor()

    sql_request.execute(f"""
    CREATE TABLE IF NOT EXISTS tests_info (
    id integer PRIMARY KEY AUTOINCREMENT,
    topic_title varchar(64),
    time_to_pass integer,
    topic_status varchar(64),
    questions integer
    );""")


create_directories()
create_db_and_base_table()
