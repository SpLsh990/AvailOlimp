"""
что бы поднять: pip install flask-sqlalchemy flask-migrate
команды:
add_new_user
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import foreign

from valid_or_not import email_is_valid
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=False, unique=True)
    elo = db.Column(db.Integer, default=-1)
    register_day = db.Column(db.DateTime, default=lambda: datetime.now().replace(second=0, microsecond=0))
    last_entry = db.Column(db.DateTime, nullable=False,
                           default=lambda: datetime.now().replace(second=0, microsecond=0))

    @staticmethod
    def register_user(email, password, nickname):
        try:
            is_valid, result = email_is_valid(email)
            if not is_valid:
                return ("error", result)
            exist_user = User.query.filter_by(email=result).first() or User.query.filter_by(nickname=nickname).first()
            if not exist_user:
                h_password = hashpw(password.encode(), gensalt(rounds=12))
                new_user = User(email=email, password=h_password, nickname=nickname)
                db.session.add(new_user)
                db.session.commit()
                return ("success", new_user.id)
            else:
                return ("error", "User already exists")
        except Exception as e:
            return ("error", str(e))

    @staticmethod
    def login_user(email, password):
        is_valid, result = email_is_valid(email)
        if not is_valid:
            return ("error", result)
        exist_user = User.query.filter_by(email=result).first()
        if exist_user:
            if checkpw(password.encode(), exist_user.password):
                exist_user.last_entry = datetime.now().replace(second=0, microsecond=0)
                db.session.commit()
                return ("success", exist_user)
            else:
                return ("error", "Wrong answer")
        else:
            return ("error", "Current user does not exist")


class Problem(db.Model):
    __tablename__ = "problems"
    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(500), nullable=False, unique=True)
    right_answer = db.Column(db.String(50), nullable=False)
    attachment = db.Column(db.String(100))

    @staticmethod
    def add_problem(object, condition, right_answer, attachment):
        if not Problem.query.filter_by(condition=condition).first():
            new_problem = Problem(object=object, condition=condition, right_answer=right_answer, attachment=attachment)
            db.session.add(new_problem)
            db.session.commit()
            return ("success", "The problem has been added successfully")
        return ("error", "An error occurred or this problem already exists")
    @staticmethod
    def get_problem(id):
        problem = Problem.query.filter_by(id=id).first()
        return problem


class SolvedProblem(db.Model):
    __tablename__ = "solvedproblems"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"))

    # Добавление и проверка решенной задачи в "копилку"
    @staticmethod
    def add_solved_problem(user_id, user_answer, problem_id):
        right_answer = Problem.query.filter_by(id=problem_id).first()
        if user_answer == right_answer.right_answer:
            solved_problem = SolvedProblem(user_id=user_id, problem_id=problem_id)
            db.session.add(solved_problem)
            db.session.commit()
            return ("success", "The problem has been solved")
        return ("error", "Worng answer or error occured")

