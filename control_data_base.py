"""
что бы поднять: pip install flask-sqlalchemy flask-migrate
команды:
add_new_user
"""

from flask_sqlalchemy import SQLAlchemy
from valid_or_not import email_is_valid
from bcrypt import hashpw, gensalt, checkpw

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=False, unique=True)

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
                return ("success", exist_user)
            else:
                return ("error", "Wrong answer")
        else:
            return ("error", "Current user does not exist")
