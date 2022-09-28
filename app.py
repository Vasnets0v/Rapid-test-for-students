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
databases_path = main_app_path + '/static/img_database'
app.config["IMAGE_UPLOADS"] = databases_path

import models
import funcs


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    flash('Спочатку необхідно авторизуватися')
    return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', topics=funcs.get_all_info_about_topics())


@app.route('/select_topic', methods=['POST', 'GET'])
@login_required
def select_topic():
    return render_template('select_topic_for_create_test.html', table_list=funcs.get_all_topics())


@app.route('/check_results', methods=['POST', 'GET'])
def check_results():
    return render_template('check_results.html', topics=funcs.get_all_topics())


@app.route('/remove_topic', methods=['POST', 'GET'])
def remove_topic():
    if request.method == 'POST':
        topic = request.form.get('topic')

        if topic:
            sql_request.execute(f'DROP TABLE {topic}')
            sql_request.execute(f'DROP TABLE score_for_theme_{topic}')
            sql_request.execute(f'DELETE FROM tests_info WHERE topic_title="{topic}"')
            db.commit()
            flash(f'Тема {topic} видалена')
            return redirect('/admin_panel')
        else:
            flash('Відсутня тема')
            return redirect('/')

    else:
        flash('Error')
        return redirect('/')


@app.route('/score', methods=['POST', 'GET'])
def score():
    if request.method == 'POST':
        topic = request.form.get('topic')
        users_score = sql_request.execute(f"SELECT * FROM score_for_theme_{topic}")

        users = []

        for user in users_score:
            users.append(user)

        return render_template('score.html', topic=topic, users=users)


@app.route('/change_password', methods=['POST', 'GET'])
def change_password():
    if request.method == 'POST':
        email = request.form.get('email')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        re_password = request.form.get('re_password')

        if new_password == re_password:
            user = db_alchemy.session.query(models.User).filter_by(email=email).first()
            if user:
                if check_password_hash(user.password, old_password):
                    password_hash = generate_password_hash(new_password)

                    user.password = password_hash
                    db_alchemy.session.commit()

                    flash('Пароль успішно змінено')
                    return redirect('/admin_panel')

                else:
                    flash('старий пароль не вірний')
                    return redirect('/admin_panel')

            else:
                flash('користувача не знайдено')
                return redirect('/admin_panel')

        else:
            flash('паролі не співпадають')
            return redirect('/admin_panel')


@app.route('/select_topic_for_student', methods=['POST', 'GET'])
def select_topic_for_student():
    if request.method == 'POST':
        topic = request.form.get('topic')
        topic_status = sql_request.execute(f'SELECT topic_status FROM '
                                           f'tests_info WHERE topic_title = "{topic}"').fetchone()

        if topic_status[0] == "closed":
            flash('Тема закрита!')
            return redirect('/')

    else:
        flash('Недостатньо прав')
        return redirect('/')

    return render_template('select_topic_for_student.html', topic=topic)


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

    return render_template('admin_panel.html', topics=funcs.get_all_info_about_topics())


@app.route('/setting_test', methods=['POST', 'GET'])
@login_required
def setting_test():
    if request.method == 'POST':
        topic = request.form.get('topic')
        time_to_pass = request.form.get('time')
        questions = request.form.get('questions')
        status = request.form.get('status')

        total_questions_in_topic = sql_request.execute(f"SELECT * FROM {topic} WHERE "
                                                       f"id=(SELECT max(id) FROM {topic});").fetchone()

        if total_questions_in_topic is None or total_questions_in_topic[0] < int(questions):
            flash('Недостатньо питань в темі')
            return redirect('/admin_panel')

        else:
            sql_request.execute(f"""UPDATE tests_info SET time_to_pass='{time_to_pass}', topic_status='{status}', 
                                questions='{questions}' WHERE topic_title='{topic}'""")
            db.commit()

        return redirect('/admin_panel')


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

    topic = request.form.get('topic')
    student_name = request.form.get('student_name')
    group = request.form.get('group')
    number_of_tests = sql_request.execute(f'SELECT questions FROM tests_info WHERE topic_title="{topic}"').fetchone()[0]

    if number_of_tests == 0:
        flash('Питання відсутні')
        return redirect('/')

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
        end_time = time.strftime("%d.%m.%Y %H:%M")

        sql_request.execute(f"""INSERT INTO score_for_theme_{topic} (user_name, user_group, percentage_score, end_time)
                                VALUES ('{user_name}', '{group}', '{result}', '{end_time}');""")
        db.commit()
        flash("Ваш результат збережено")

    else:
        flash('it do not work')
        return redirect('/')
    return redirect('/')


@app.route('/save_new_test', methods=['POST', 'GET'])
@login_required
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
    flash("Тести успішно збережені")

    return redirect('/')


# БАГ! при створенні таблиці з числовою назвою та коли є пробіли в назві
@app.route('/create_test', methods=['POST', 'GET'])
@login_required
def new_test():

    if request.method == 'POST':
        new_topic = request.form.get('topic')

        if new_topic:
            models.table_for_new_topic(new_topic)
            models.student_score(new_topic)

            sql_request.execute(f""" INSERT INTO tests_info (topic_title, time_to_pass, topic_status, questions)
            VALUES ('{new_topic}', 0, 'closed', 0)""")

            db.commit()

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
