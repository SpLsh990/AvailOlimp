import os
import flask
from blueprints.main import main_bp
from control_data_base import db
from add_problems import add_problems


def create_app():
    app = flask.Flask(__name__)

    app.secret_key = os.environ.get('SECRET_KEY', 'secret key')

    database_url = os.environ.get('DATABASE_URL')

    # Для Render
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    # Для локальной разработки
    if not database_url:
        database_url = 'sqlite:///mydatabase.db'
        print("Warning: Using SQLite database. Set DATABASE_URL for PostgreSQL.")

    app.config.update(
        SESSION_TYPE='filesystem',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true',
        PERMANENT_SESSION_LIFETIME=3600,
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()
        add_problems()

    app.register_blueprint(main_bp)
    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)