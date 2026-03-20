from flask import Flask, render_template, Blueprint, request, session, redirect
from control_data_base import User

main_bp = Blueprint('main_bp', __name__,
                    template_folder='../templates/main',
                    static_folder='../static')


@main_bp.route('/')
def index():
    return render_template('index.html',
                           title="AvailOlimp", main_bp=main_bp)


@main_bp.route('/form_register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('form_register.html', title="Register Form", main_bp=main_bp)

    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nickname = request.form['nickname']
        answer = User.register_user(email, password, nickname)
        if answer[0] == "success":
            session['user_id'] = answer[1]
            session['nickname'] = nickname
            return redirect('/')
        else:
            print(answer)
        return answer


@main_bp.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Login Form", main_bp=main_bp)
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        answer = User.login_user(email, password)
        if answer[0] == "success":
            session['user_id'] = answer[1].id
            session['nickname'] = answer[1].nickname
            return redirect('/')


@main_bp.route('/logout.html')
def logout():
    session.clear()
    return redirect('/')
