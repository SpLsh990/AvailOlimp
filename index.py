import flask
from blueprints.main import main_bp
from control_data_base import db


def create_app():
    app = flask.Flask(__name__)

    app.secret_key = "secret key"
    app.config.update(
        SESSION_TYPE='filesystem',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False,
        PERMANENT_SESSION_LIFETIME=3600,
        SQLALCHEMY_DATABASE_URI='sqlite:///mydatabase.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
