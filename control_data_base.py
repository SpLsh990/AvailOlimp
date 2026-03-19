"""
что бы поднять: pip install flask-sqlalchemy flask-migrate
команды:
add_new_user
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.testing.pickleable import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Main_db(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=False)

    @staticmethod
    def register_user(email, password, nickname):
        with app.app_context():
            try:
                exist_user_email = Main_db.query.filter_by(email=email).first()
                exist_user_nickname = Main_db.query.filter_by(email=email).first()
                if not exist_user_nickname and not exist_user_email:
                    new_user = Main_db(email=email, password=password,  nickname=nickname)
                    db.session.add(new_user)
                    db.session.commit()
                    return "success"
                elif exist_user_email:
                    return ("error", "User with this email already exists")
                elif exist_user_nickname:
                    return ("error", "User with this nickname already exists")
                else:
                    return ("error", "User already exists")
            except Exception as e:
                return ("error", str(e))
if "__main__" == __name__:
    with app.app_context():
        db.create_all()
