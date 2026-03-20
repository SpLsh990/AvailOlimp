import flask
from blueprints.main import main_bp
from control_data_base import db


def create_app():
    app = flask.Flask(__name__)

    # Добавляем конфигурацию
    app.secret_key = "secret key"
    app.config.update(
        SESSION_TYPE='filesystem',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False,
        PERMANENT_SESSION_LIFETIME=3600,
        SQLALCHEMY_DATABASE_URI='sqlite:///mydatabase.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Инициализируем БД с приложением
    db.init_app(app)

    # Создаем таблицы
    with app.app_context():
        db.create_all()

    # Регистрируем blueprint
    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
