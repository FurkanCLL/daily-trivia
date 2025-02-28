from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()
UTC = timezone.utc

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    was_asked = db.Column(db.Boolean, default=False)

class DailyQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    date = db.Column(db.Date, default=lambda: datetime.now(UTC))  # UTC hatası düzeltilmiş hali

class Stats(db.Model):
    date = db.Column(db.Date, primary_key=True)
    total_players = db.Column(db.Integer, default=0)
