from flask import Flask, render_template, request, redirect
import sys
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('database.s3db', check_same_thread=False)
sql_request = db.cursor()


def create_new_table(new_topic):
    sql_request.execute(f"""
    CREATE TABLE IF NOT EXISTS {new_topic} (
        id integer PRIMARY KEY AUTOINCREMENT,
        question varchar,
        answer_1 varchar,
        answer_2 varchar,
        answer_3 varchar,
        answer_4 varchar,
        answer_5 varchar,
        answer_6 varchar,
        right_answer integer
        );""")


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/select_topic', methods=['POST', 'GET'])
def select_topic():
    all_table_content = sql_request.execute("SELECT * FROM sqlite_master WHERE type='table'")
    table_list = []
    for i in all_table_content:
        table_list.append(i[1])
    return render_template('select_topic.html', table_list=table_list)


@app.route('/save_new_test', methods=['POST', 'GET'])
def save_test():
    print(request.form['total_answers_1'])
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
