import sqlite3


def get_data_from_setting():
    with sqlite3.connect('main_db.s3db', check_same_thread=False) as db:
        sql_request = db.cursor()

        r = sql_request.execute(f"""SELECT * FROM tests_info;""")

        return r


def generate_array_id_and_name():
    tables = get_data_from_setting()
    name_and_id = []

    for table in tables:
        name_and_id.append([table[0], table[1]])

    return name_and_id


def rename_table(names):

    with sqlite3.connect('main_db.s3db', check_same_thread=False) as db:
        sql_request = db.cursor()

    for topic in names:
        try:
            sql_request.execute(f"""ALTER TABLE score_for_theme_{topic[1]} RENAME TO score_{topic[0]};""")
        except sqlite3.OperationalError:
            print('Error rename')

    db.commit()


name_and_id = generate_array_id_and_name()
rename_table(name_and_id)
# print(name_and_id)



