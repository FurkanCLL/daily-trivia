import csv
from models import db, Question

def import_questions_from_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            existing_question = Question.query.filter_by(question_text=row['question_text']).first()
            if existing_question:
                continue

            new_question = Question(
                question_text=row['question_text'],
                option_a=row['option_a'],
                option_b=row['option_b'],
                option_c=row['option_c'],
                option_d=row['option_d'],
                correct_option=row['correct_option'],
                category=row['category']
            )
            db.session.add(new_question)
        db.session.commit()
    print("Questions imported successfully!")