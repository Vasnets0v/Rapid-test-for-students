from flask import render_template, request, redirect, flash, send_file
import os
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user
import models
import funcs
from funcs import ExelSheet
from __init__ import app, login_manager, get_db, db_alchemy

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
    topics = funcs.get_all_topics()
    clear_topics = funcs.get_array_clear_topics(topics)
    topic_dict = dict(zip(topics, clear_topics))
    return render_template('check_results.html', topic_dict=topic_dict)


@app.route('/select_test_to_edit', methods=['POST', 'GET'])
@login_required
def select_test_to_edit():
    topics = funcs.get_all_topics()
    clear_topics = funcs.get_array_clear_topics(topics)
    topic_dict = dict(zip(topics, clear_topics))
    return render_template('select_test_to_edit.html', topic_dict=topic_dict)


@app.route('/new_user', methods=['POST', 'GET'])
@login_required
def new_user():
    return render_template('new_user.html')


@app.route('/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    return render_template('change_password.html')


@app.route('/setting', methods=['POST', 'GET'])
@login_required
def setting():
    return render_template('setting_main_page.html')


@app.route('/tests_settings', methods=['POST', 'GET'])
@login_required
def tests_settings():
    return render_template('tests_settings.html', topics=funcs.get_all_info_about_topics())


@app.route('/edit_test', methods=['POST', 'GET'])
@login_required
def edit_test():
    if request.method == 'POST':
        topic = request.form.get('topic')
        content = funcs.get_all_records_from_table(topic)
        num_of_records = funcs.get_num_of_records_in_table(topic)
        return render_template('edit_test.html', content=content, topic=topic, num_of_records=num_of_records)
    else:
        flash('Error')
        return redirect('/')


@app.route('/deletion_confirmation', methods=['POST', 'GET'])
@login_required
def deletion_confirmation():
    if request.method == 'POST':
        topic = request.form.get('topic')
        return render_template('deletion_confirmation.html', topic=topic)
    else:
        flash('Error')
        return redirect('/')


@app.route('/reset_score', methods=['POST'])
@login_required
def reset_score():
    if request.method == 'POST':
        topic = request.form.get('topic')

        db = get_db()
        db.cursor().execute(f'DROP TABLE score_for_theme_{topic}')
        db.commit()

        models.student_score(topic)

        flash(f'Записи в таблиці {topic} видалені')
        return redirect('/')
    else:
        flash('Error')
        return redirect('/')


@app.route('/download_sheet', methods=['POST'])
@login_required
def download_sheet():
    if request.method == 'POST':
        db = get_db()
        sql_request = db.cursor()
        topic = request.form.get('topic')
        sheet = ExelSheet(topic, sql_request)
        sheet.insert_user_data()
        name = sheet.file_name + '.xlsx'
        return send_file(name, as_attachment=True)
    else:
        flash('Error')
        return redirect('/')


@app.route('/handle_edit_test_page', methods=['POST'])
@login_required
def handle_edit_test_page():
    if request.method == 'POST':
        topic = request.form.get('topic')
        num_of_question = request.form.get('num_of_records')
        ids_edited_records = request.form.getlist('edited_checkbox')

        # request return real index from database
        index_deleted_records = request.form.get('delete_question').split('_')

        db = get_db()

        for id in index_deleted_records:
            db.cursor().execute(f"DELETE FROM {topic} WHERE id = '{id}'")

        for id in ids_edited_records:
            table_id = request.form.get(f'database_table_id_{int(id)}')
            question = request.form.get(f'question_{int(id)}')
            answers = []

            for answer in range(6):
                answers.append(request.form.get(f'answer_{int(id)}_{answer + 1}'))

            db.cursor().execute(f"UPDATE {topic} SET question = '{question}', answer_1 = '{answers[0]}', answer_2 = '{answers[1]}',"
                                f"answer_3 = '{answers[2]}', answer_4 = '{answers[3]}', answer_5 = '{answers[4]}'," 
                                f"answer_6 = '{answers[5]}' WHERE id = '{table_id}' ")

        db.commit()
                
        flash('Зміни збережено')
        return redirect('/')
    else:
        flash('Error')
        return redirect('/')


@app.route('/remove_topic', methods=['POST', 'GET'])
def remove_topic():
    if request.method == 'POST':
        topic = request.form.get('topic')

        if topic:
            db = get_db()
            db.cursor().execute(f'DROP TABLE {topic}')
            db.cursor().execute(f'DROP TABLE score_for_theme_{topic}')
            db.cursor().execute(f'DELETE FROM tests_info WHERE topic_title="{topic}"')
            db.commit()

            flash(f'Тема {topic} видалена')
            return redirect('/setting')
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
        clear_topic = funcs.get_clear_topic_name(topic)

        db = get_db()
        users_score = db.cursor().execute(f"SELECT * FROM score_for_theme_{topic} order by id desc")
        db.commit()

        users = [user for user in users_score]

        return render_template('score.html', topic=topic, users=users, clear_topic=clear_topic)


@app.route('/handle_change_password_page', methods=['POST', 'GET'])
def handle_change_password_page():
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
                    return redirect('/setting')

                else:
                    flash('старий пароль не вірний')
                    return redirect('/setting')

            else:
                flash('користувача не знайдено')
                return redirect('/setting')

        else:
            flash('паролі не співпадають')
            return redirect('/setting')


@app.route('/select_topic_for_student', methods=['POST', 'GET'])
def select_topic_for_student():
    if request.method == 'POST':
        topic_id = request.form.get('topic_id')

        db = get_db()
        topic_status = db.cursor().execute(f'SELECT topic_status FROM '
                                           f'tests_info WHERE id = "{topic_id}"').fetchone()
        db.commit()
        

        if topic_status[0] == "closed":
            flash('Тема закрита!')
            return redirect('/')

    else:
        flash('Недостатньо прав')
        return redirect('/')

    return render_template('select_topic_for_student.html', topic_id=topic_id)


@app.route('/handle_new_user_page', methods=['POST', 'GET'])
@login_required
def handle_new_user_page():
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
                return redirect('/setting')
        else:
            flash('Паролі не співпадають')
            return redirect('/setting')
    else:
        flash('Error')
        return redirect('/')


@app.route('/handle_setting_test_page', methods=['POST', 'GET'])
@login_required
def handle_setting_test_page():
    if request.method == 'POST':
        topic_id = request.form.get('topic_id')
        topic = funcs.conver_topic_id_into_title(topic_id)
        time_to_pass = request.form.get('time')
        questions = request.form.get('questions')
        status = request.form.get('status')

        db = get_db()
        total_questions_in_topic = db.cursor().execute(f"SELECT * FROM {topic} WHERE "
                                                       f"id=(SELECT max(id) FROM {topic});").fetchone()

        if total_questions_in_topic is None or total_questions_in_topic[0] < int(questions):
            flash('Недостатньо питань в темі')

            

            return redirect('/setting')

        else:
            db.cursor().execute(f"""UPDATE tests_info SET time_to_pass='{time_to_pass}', topic_status='{status}', 
                                questions='{questions}' WHERE topic_title='{topic}'""")
            db.commit()
            

            flash('Зміни збережено')

        return redirect('/setting')
    else:
        flash('Error')
        return redirect('/')


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = models.User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect('/setting')
            else:
                flash('Неправильний логін або пароль')
        else:
            flash('Неправильний логін або пароль')

    return render_template('login.html')


@app.route('/testing', methods=['POST', 'GET'])
def testing():

    topic_id = request.form.get('topic_id')
    topic = funcs.conver_topic_id_into_title(topic_id)
    student_name = request.form.get('student_name')
    group = request.form.get('group')

    db = get_db()
    number_of_tests = db.cursor().execute(f'SELECT questions FROM tests_info WHERE id="{topic_id}"').fetchone()[0]
    

    if number_of_tests == 0:
        flash('Питання відсутні')
        return redirect('/')

    if topic_id and student_name and group:
        content = funcs.get_question_from_db(number_of_tests, topic_id)

        test_ids = []

        for i in content:
            test_ids.append(i)

            #change numbers to variables
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

        db = get_db()

        for test_id in test_ids:
            answers_from_db = db.cursor().execute(f'SELECT right_answer FROM {topic} WHERE id = {int(test_id)}')
            correct_answers[test_id] = answers_from_db.fetchone()[0]

            user_answers[int(test_id)] = request.form.get(f'radio_{test_id}')

        result = funcs.process_user_result(correct_answers, user_answers)
        end_time = time.strftime("%d.%m.%Y %H:%M")

        db.cursor().execute(f"""INSERT INTO score_for_theme_{topic} (user_name, user_group, percentage_score, end_time)
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

        db = get_db()
        db.cursor().execute(f'INSERT INTO {topic} (question, answer_1, answer_2, answer_3, answer_4, answer_5, '
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

            db = get_db()
            db.cursor().execute(f""" INSERT INTO tests_info (topic_title, time_to_pass, topic_status, questions)
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
