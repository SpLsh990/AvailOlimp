"""
что бы поднять: pip install flask-sqlalchemy flask-migrate
команды:
add_new_user
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)

    @staticmethod
    def register_user(email, password, nickname):
        """
        продумать систему регистрации, можно править не только бд. Сейчас register_user возвращает два параметра:
        1) статус регистрации
        2) ID - он ОБЯЗАТЕЛЬНО должна возвращать эта функция, она нужна для сессий
        """
        try:
            exist_user_email = User.query.filter_by(email=email).first()
            exist_user_nickname = User.query.filter_by(nickname=nickname).first()
            if not exist_user_nickname and not exist_user_email:
                new_user = User(email=email, password=password, nickname=nickname)
                db.session.add(new_user)
                db.session.commit()
                return ("success", new_user.id)
            elif exist_user_email:
                return ("error", "User with this email already exists")
            elif exist_user_nickname:
                return ("error", "User with this nickname already exists")
            else:
                return ("error", "User already exists")
        except Exception as e:
            return ("error", str(e))

    @staticmethod
    def login_user(email, password):
        """
        Здесь уже с 0 думай, обязательно нужен ID а дальше мучаться тебе)
        Пока функция статично выдает успех и класс юзера из бд, почта которого совпала
        Так же нету обработок отсутствия почты(
        """
        return ("success", User.query.filter_by(email=email).first())
