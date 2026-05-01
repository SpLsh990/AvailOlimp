from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import foreign
from valid_or_not import email_is_valid
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime
import re

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


# Problem: class для добавления задач
class Problem(db.Model):
    __tablename__ = "problems"
    """
    id - id
    object - объект (math / physics) | обязательно
    title - название | обязательно
    condition - условие задачи | обязательно
    right_answer - правильный ответ | обязательно
    attachment - название фото в папке static/images/ | не обязательно, по умолчанию: ""
    """
    id = db.Column(db.Integer, primary_key=True)
    object = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(500), nullable=False, unique=True)
    right_answer = db.Column(db.String(50), nullable=False)
    attachment = db.Column(db.String(100))

    # add_problem - метод для добавления задачи
    @staticmethod
    def add_problem(object: str, title: str, condition: str, right_answer: str,
                    attachment="") -> tuple:
        # если задачи еще нет, то добавляем
        if not Problem.query.filter_by(condition=condition).first():
            new_problem = Problem(object=object, title=title, condition=condition, right_answer=right_answer,
                                  attachment=attachment)
            db.session.add(new_problem)
            db.session.commit()
            return ("success", "The problem has been added successfully")
        return ("error", "An error occurred or this problem already exists")

    # метод для получения класса с нужной задачей по ее id
    @staticmethod
    def get_problem(id: int):
        problem = Problem.query.filter_by(id=id).first()
        return problem

    @staticmethod
    def get_random_problem(object: str):
        random_problem = Problem.query.order_by(object=object).order_by(db.random()).first()
        return random_problem


# SolvedProblem: class, для связи юзера и решенных задач
class SolvedProblem(db.Model):
    __tablename__ = "solvedproblems"
    """
    id - id
    user_id - id юзера в таблице users
    problem_id - id задачи в таблице problems_id
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    problem_id = db.Column(db.String, db.ForeignKey("problems.id"))

    # метод для добавления новой решенной задачи
    @staticmethod
    def add_solved_problem(user_id: int, user_answer: str, problem_id: int) -> tuple:
        # инициализация двух бд
        problem = Problem.query.filter_by(id=problem_id).first()
        solved_problem = SolvedProblem.query.filter_by(user_id=user_id).first()
        # если ответ верный и у юзера нет верно решенных задач
        # задачи инициализируются в виде строки: "id_решенной_задачи"
        print(solved_problem)
        user_answer = user_answer.replace(".", ",").rstrip()  # Чтобы было неважно, через запятую или точку вводить ответы
        if user_answer == problem.right_answer and solved_problem is None:
            solved_problem = SolvedProblem(user_id=user_id, problem_id=str(problem_id))
            db.session.add(solved_problem)
            db.session.commit()
            return ("success", "The problem has been solved")
        # если ответ верный и у юзера есть решенные задачи
        # задачи добавляются через запятую в виде "id_решенной_задачи1,id_решенной_задачи2"
        elif user_answer == problem.right_answer and solved_problem is not None:
            """
            solved_problem_data: list
            solved_problem_data = [id_решенной_задачи1, id_решенной_задачи2]
            """
            solved_problem_data = solved_problem.problem_id.split(",")
            # если задачи нет в решенных, добавляем
            if problem_id not in solved_problem_data:
                solved_problem.problem_id = solved_problem.problem_id + "," + str(problem_id)
                db.session.commit()
                return ("success", "The problem has been solved in list")
            # если есть, ошибка: The problem is already solved
            else:
                return ("error", "The problem is already solved")
        # ответ неверный
        return ("error", "Worng answer or error occured")

    # метод для получения всех решенных задач юзера
    @staticmethod
    def get_solved_problems(user_id: int) -> list:
        solved_problems = SolvedProblem.query.filter_by(user_id=user_id).first()
        if solved_problems is None:
            return []
        return solved_problems.problem_id.split(",")
