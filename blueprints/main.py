from flask import Flask, render_template, Blueprint, request, session, redirect
from control_data_base import User, Problem, SolvedProblem

main_bp = Blueprint('main_bp', __name__,
                    template_folder='../templates/main',
                    static_folder='../static')


@main_bp.route('/')
def index():
    if session.get('user_id'):
        return render_template('index.html',
                               title="AvailOlimp", main_bp=main_bp)
    else:
        session.clear()
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
            session['error_password_email'] = True
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


@main_bp.route("/physic_1.html", methods=['GET', 'POST'])
def physic_1():
    if request.method == 'GET':
        problem = Problem.get_problem(1)
        return render_template("physic_1.html",
                               subject=problem.object,
                               task_text=problem.condition,
                               task_image=problem.attachment)

    elif request.method == 'POST':
        answer = request.form['answer']
        print(answer)
        server_answer = SolvedProblem.add_solved_problem(session.get('user_id'), answer, 1)
        if server_answer[0] == "success":
            session['correct_1'] = True
        else:
            session['incorrect_1'] = True
    return redirect('/physic_1.html')

