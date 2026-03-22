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
            session['email'] = email
            session['nickname'] = answer[1].nickname
            return redirect('/')
        else:
            session['password_error'] = False
            session['session.error_user_exist'] = False
            if answer[1] == "Wrong password":
                session['password_error'] = True
                return redirect('/login.html')
            elif answer[1] == "Current user does not exist":
                session['error_user_exist'] = True
                return redirect('/login.html')

@main_bp.route('/pvp_mode.html')
def pvp_mode():
    if session.get('user_id') is None:
        return redirect('/login.html')
    else:
        return render_template('pvp_mode.html')

@main_bp.route('/physics_mode.html')
def physics_mode():
    if session.get('user_id') is None:
        return redirect('/login.html')
    else:
        return render_template('physic_mode.html')

@main_bp.route('/math_mode.html')
def math_mode():
    if session.get('user_id') is None:
        return redirect('/login.html')
    else:
        return render_template('math_mode.html')

@main_bp.route('/logout.html')
def logout():
    session.clear()
    return redirect('/')
