import os
from datetime import date, datetime, timedelta
import pytz
import random
from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Question, DailyQuestion, Stats
from import_csv import import_questions_from_csv
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


db.init_app(app)

def check_and_import_questions():
    question_count = Question.query.count()
    if question_count == 0:
        csv_path = "data/Questions.csv"
        if os.path.exists(csv_path):
            import_questions_from_csv(csv_path)
            print("CSV file imported automatically!")
        else:
            print("CSV file not found, skipping import.")

def select_daily_questions():
    today = date.today()

    existing_questions = DailyQuestion.query.filter_by(date=today).count()
    if existing_questions >= 5:
        print("Daily questions already selected.")
        return

    available_questions = Question.query.filter_by(was_asked=False).all()

    if len(available_questions) < 5:
        db.session.query(Question).update({Question.was_asked: False})
        db.session.commit()
        available_questions = Question.query.filter_by(was_asked=False).all()

    selected_questions = random.sample(available_questions, 5)

    for question in selected_questions:
        daily_question = DailyQuestion(question_id=question.id, date=today)
        db.session.add(daily_question)
        question.was_asked = True
        db.session.add(question)

    db.session.commit()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questions/<int:question_index>')
def show_question(question_index):
    today = date.today()

    if question_index == 0:
        session['correct_count'] = 0
        session['user_answers'] = {}

    daily_questions = db.session.query(Question).join(DailyQuestion).filter(DailyQuestion.date == today).all()

    if 0 <= question_index < len(daily_questions):
        question = daily_questions[question_index]
        return render_template('question.html', question=question, question_index=int(question_index), total_questions=len(daily_questions))

    return redirect(url_for('show_results'))


@app.route('/submit_answer/<question_index>', methods=['POST'])
def submit_answer(question_index):
    today = date.today()

    try:
        question_index = int(question_index)
    except ValueError:
        return redirect(url_for('show_results'))

    user_choice = request.form.get("answer")

    daily_questions = db.session.query(Question).join(DailyQuestion).filter(DailyQuestion.date == today).all()

    if 0 <= question_index < len(daily_questions):
        question = daily_questions[question_index]
        user_answers = session.get('user_answers', {})
        user_answers[str(question.id)] = user_choice
        session['user_answers'] = user_answers

        correct_count = session.get('correct_count', 0)
        if user_choice == question.correct_option:
            correct_count += 1
        session['correct_count'] = correct_count

        return redirect(url_for('show_question', question_index=question_index + 1))

    return redirect(url_for('show_results'))


@app.route('/results')
def show_results():
    today = date.today()
    correct_count = session.get('correct_count', 0)
    user_answers = session.get('user_answers', {})


    daily_stat = Stats.query.filter_by(date=today).first()
    if not daily_stat:
        daily_stat = Stats(date=today, total_players=1)
        db.session.add(daily_stat)
    else:
        daily_stat.total_players += 1
    db.session.commit()


    utc_tz = pytz.utc
    now = datetime.now(utc_tz)
    tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    time_remaining = int((tomorrow - now).total_seconds())

    return render_template('results.html',
                           correct_count=correct_count,
                           total_players=daily_stat.total_players,
                           time_remaining=time_remaining)


@app.route('/about')
def about():
    return render_template('about.html')


@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        check_and_import_questions()
        select_daily_questions()
    app.run(host="0.0.0.0", port=5000)
