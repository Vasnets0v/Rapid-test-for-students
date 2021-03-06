from flask import Flask, render_template, request, redirect
import sys
import sqlite3
import os
import time
import random

app = Flask(__name__)

if os.path.exists("databases"):
    pass
else:
    os.mkdir("databases")

if os.path.exists("databases/img"):
    pass
else:
    os.mkdir("databases/img")

main_app_path = os.path.dirname(os.path.abspath(__file__))
databases_path = main_app_path + '\databases\img'
app.config["IMAGE_UPLOADS"] = databases_path

db = sqlite3.connect('databases/main_db.s3db', check_same_thread=False)
sql_request = db.cursor()


def create_new_table(new_topic):
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
        right_answer varchar(255),
        testing_time varchar(255),
        num_display_questions varchar(255)
        );""")


def get_tables_from_db():
    all_table_content = sql_request.execute("SELECT * FROM sqlite_master WHERE type='table'")
    table_list = []
    for i in all_table_content:
        if i[1] == 'sqlite_sequence':
            continue
        else:
            table_list.append(i[1])
    return table_list


def get_content_from_db(num_of_questions, topic):
    sql_request.execute(f"SELECT count(*) FROM {topic}")
    total_columns = sql_request.fetchone()[0] + 1

    random_ids = random.sample(range(1, total_columns), num_of_questions)

    content = {}
    for i in range(num_of_questions):
        sql_request.execute(f"SELECT question, img_question, answer_1, answer_2, answer_3, answer_4, "
                            f"answer_5, answer_6, img_1, img_2, img_3, img_4, img_5, img_6 FROM {topic} "
                            f"WHERE id = '{random_ids[i]}'")
        content[random_ids[i]] = sql_request.fetchone()
    print(content)
    return content


def save_img(new_img):
    current_time = str(time.time())
    raw_img_name = current_time.split('.')
    old_img_name = new_img.filename.split('.')
    name = raw_img_name[0] + raw_img_name[1] + "." + old_img_name[1]
    new_img.filename = name

    new_img.save(os.path.join(app.config["IMAGE_UPLOADS"], new_img.filename))
    return name


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/select_topic_for_student', methods=['POST', 'GET'])
def select_topic_for_student():
    table_list = get_tables_from_db()
    return render_template('select_topic_for_student.html', table_list=table_list)


@app.route('/select_topic', methods=['POST', 'GET'])
def select_topic():
    table_list = get_tables_from_db()
    return render_template('select_topic_for_create_test.html', table_list=table_list)


@app.route('/testing', methods=['POST', 'GET'])
def testing():
    try:
        topic = request.form['select_topic']
    except Exception:
        return "You don't have permissions!"

    if topic:
        get_content_from_db(3, topic)
        return render_template('testing.html', topic=topic)


@app.route('/save_new_test', methods=['POST', 'GET'])
def save_test():

    topic = request.form['topic_test']
    total_questions = int(request.form['total_questions'])

    for i in range(total_questions):
        question_id = i + 1
        question = request.form[f'question_{question_id}']
        img_question = request.files[f'q_image_{question_id}']

        if img_question:
            new_img_question_name = save_img(img_question)
        else:
            new_img_question_name = "NULL"

        answers = []
        correct_answer = '0 '
        img_answers = []

        total_answers = int(request.form[f'total_answers_{question_id}'])

        for j in range(total_answers):
            num = j + 1

            temp_answer = request.form[f'answer_{question_id}_{num}']

            if temp_answer == '':
                answers.append('NULL')
            else:
                answers.append(temp_answer)

            img = request.files[f'image_{question_id}_{num}']
            if img:
                new_img_name = save_img(img)
                img_answers.append(new_img_name)
            else:
                img_answers.append('NULL')

            try:
                temp_trash = request.form[f'checkbox_{question_id}_{num}']
                correct_answer += f"{num}" + " "
            except Exception:
                pass

        for _ in range(6 - total_answers):
            answers.append('NULL')
            img_answers.append('NULL')

        sql_request.execute(f'INSERT INTO {topic} (question, answer_1, answer_2, answer_3, answer_4, answer_5, '
                            f'answer_6, right_answer, img_1, img_2, img_3, img_4, img_5, img_6, img_question) '
                            f'VALUES ("{question}", "{answers[0]}", "{answers[1]}", "{answers[2]}", "{answers[3]}", '
                            f'"{answers[4]}", "{answers[5]}", "{correct_answer}", "{img_answers[0]}", '
                            f'"{img_answers[1]}", "{img_answers[2]}", "{img_answers[3]}", "{img_answers[4]}"'
                            f', "{img_answers[5]}", "{new_img_question_name}")')
        db.commit()

    return redirect('/')


@app.route('/create_test', methods=['POST', 'GET'])
def new_test():

    try:
        new_topic = request.form['topic']
    except Exception:
        return "You don't have permissions!"

    if new_topic != "":
        create_new_table(new_topic)
        return render_template('create_test.html', current_topic=new_topic)
    else:
        try:
            created_topic = request.form['select_topic']
        except Exception:
            return "Error, you should create topic first of all"
        return render_template('create_test.html', current_topic=created_topic)


@app.route('/create_test', methods=['POST', 'GET'])
def create_new_test():
    return render_template('create_test.html')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run(debug=True)
