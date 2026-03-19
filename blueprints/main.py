from flask import Flask, render_template, Blueprint, request
from control_data_base import Main_db

main_bp = Blueprint('main_bp', __name__,
                    template_folder='../templates/main',
                    static_folder='../static')

app = Flask(__name__)
users_bd = Main_db()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'supersecretkey'

@main_bp.route('/')
def index():
    return render_template('index.html',
                           title="AvailOlimp")

@main_bp.route('/form_register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('form_register.html')

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nickname = request.form['nickname']
        print(email, password, nickname)
        answer = users_bd.register_user(email, password, nickname)
        print(answer)
        return answer