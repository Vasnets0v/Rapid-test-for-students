from flask import Flask, render_template, request, redirect, flash
import sys
import sqlite3
import os
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_alchemy = SQLAlchemy(app)
db = sqlite3.connect('databases/main_db.s3db', check_same_thread=False)
sql_request = db.cursor()
login_manager = LoginManager(app)

main_app_path = os.path.dirname(os.path.abspath(__file__))
databases_path = main_app_path + '/databases/img'
app.config["IMAGE_UPLOADS"] = databases_path

import models
import funcs


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/select_topic_for_student', methods=['POST', 'GET'])
def select_topic_for_student():
    return render_template('select_topic_for_student.html', table_list=funcs.get_all_tables_from_db())


@app.route('/select_topic', methods=['POST', 'GET'])
def select_topic():
    return render_template('select_topic_for_create_test.html', table_list=funcs.get_all_tables_from_db())


@app.route('/check_results', methods=['POST', 'GET'])
def check_results():
    return render_template('check_results.html')


@app.route('/admin_panel', methods=['POST', 'GET'])
@login_required
def admin_panel():
    if request.method == 'POST':
        if request.form['password'] == request.form['re_password']:

            email = request.form['email']
            user = models.User.query.filter_by(email=email).first()

            if user:
                flash('Користувач з такім email вже зареєстрований')
            else:
                name = request.form["name"]
                surname = request.form["surname"]
                password_hash = generate_password_hash(request.form['password'])

                new_admin = models.User(email=email, password=password_hash, name=name,
                                        surname=surname, time_of_creation=time.time())
                db_alchemy.session.add(new_admin)
                db_alchemy.session.commit()

                flash('Користувача успішно додано')
        else:
            flash('Паролі не співпадають')

    return render_template('admin_panel.html')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/admin_panel')
            else:
                flash('Неправильний логін або пароль')
        else:
            flash('Неправильний логін або пароль')

    return render_template('login.html')


@app.route('/testing', methods=['POST', 'GET'])
def testing():
    number_of_tests = 3

    topic = request.form.get('select_topic')
    student_name = request.form.get('student_name')
    group = request.form.get('group')

    if topic and student_name and group:
        content = funcs.get_content_from_db(number_of_tests, topic)

        test_ids = []

        for i in content:
            test_ids.append(i)

            if content[i][8] == 'NULL':
                if content[i][9] == 'NULL':
                    content[i].append(funcs.get_mixed_order(3))

            elif content[i][10] == 'NULL':
                if content[i][11] == 'NULL':
                    content[i].append(funcs.get_mixed_order(4))

            elif content[i][12] == 'NULL':
                if content[i][13] == 'NULL':
                    content[i].append(funcs.get_mixed_order(5))

            else:
                content[i].append(funcs.get_mixed_order(6))

        return render_template('testing.html', topic=topic, student_name=student_name, group=group, content=content,
                               test_ids=test_ids)

    flash('Помилка, відсутня тема тестування')
    return redirect('/')


@app.route('/process_test', methods=['POST', 'GET'])
def process_test():

    if request.method == 'POST':
        topic = request.form.get('topic')
        user_name = request.form.get('student_name')
        group = request.form.get('group')

        str_test_ids = request.form['test_ids']
        test_ids = str_test_ids.strip('[]').split(', ')

        correct_answers = {}
        user_answers = {}

        for test_id in test_ids:
            answers_from_db = sql_request.execute(f'SELECT right_answer FROM {topic} WHERE id = {int(test_id)}')
            correct_answers[test_id] = answers_from_db.fetchone()[0]

            user_answers[int(test_id)] = request.form.get(f'radio_{test_id}')

        result = funcs.process_user_result(correct_answers, user_answers)

        models.create_table_for_staff_info(topic)
        sql_request.execute(f"""INSERT INTO score_for_theme_{topic} (user_name, user_group, percentage_score)
                                VALUES ('{user_name}', '{group}', '{result}');""")
        db.commit()
        flash("Ваш результат збережено")

    else:
        flash('it do not work')
        return redirect('/')
    return redirect('/')


@app.route('/save_new_test', methods=['POST', 'GET'])
def save_test():

    topic = request.form['topic_test']
    total_questions = int(request.form['total_questions'])

    for i in range(total_questions):
        question_id = i + 1
        question = request.form[f'question_{question_id}']
        img_question = request.files[f'q_image_{question_id}']

        if img_question:
            new_img_question_name = funcs.get_new_img_name(img_question.filename)
            img_question.save(os.path.join(app.config["IMAGE_UPLOADS"], new_img_question_name))
        else:
            new_img_question_name = "NULL"

        answers = []
        img_answers = []

        correct_answer = request.form.get(f'radio_{question_id}')

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
                new_img_name = funcs.get_new_img_name(img.filename)
                img.save(os.path.join(app.config["IMAGE_UPLOADS"], new_img_name))
                img_answers.append(new_img_name)
            else:
                img_answers.append('NULL')

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


# БАГ! при створенні таблиці з числовою назвою та коли є пробіли в назві
@app.route('/create_test', methods=['POST', 'GET'])
def new_test():

    if request.method == 'POST':
        new_topic = request.form.get('topic')

        if new_topic:
            models.create_new_table(new_topic)
            return render_template('create_test.html', current_topic=new_topic)
        else:
            topic = request.form.get('select_topic')
            if topic:
                return render_template('create_test.html', current_topic=topic)
            else:
                flash('Невідома помилка')
                return redirect('/')

    else:
        flash('У вас відсутні права для перегляду сторінки')
        return redirect('/')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port, debug=True)
    else:
        app.run(debug=True)
