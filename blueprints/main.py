from flask import Flask, render_template, Blueprint, request, session, redirect, jsonify
from control_data_base import User, Problem, SolvedProblem

# зависимости
main_bp = Blueprint('main_bp', __name__,
                    template_folder='../templates/main',
                    static_folder='../static')


#TODO Убрать все что для совместимости

# главный блок (index, register, login, logout)
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
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            nickname = data.get('nickname')

            answer = User.register_user(email, password, nickname)

            if answer[0] == "success":
                session['user_id'] = answer[1]
                session['email'] = email
                session['nickname'] = nickname
                return jsonify({
                    'success': True,
                    'redirect_url': '/'
                })
            else:
                error_message = answer[1]
                return jsonify({
                    'success': False,
                    'message': error_message
                }), 400
        else:
            # Старая обработка, для совместимости
            email = request.form['email']
            password = request.form['password']
            nickname = request.form['nickname']

            answer = User.register_user(email, password, nickname)

            if answer[0] == "success":
                session['user_id'] = answer[1]
                session['email'] = email
                session['nickname'] = nickname
                return redirect('/')
            else:
                session['register_error'] = answer[1]
                return redirect('/form_register.html')


@main_bp.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Login Form", main_bp=main_bp)

    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            answer = User.login_user(email, password)
            if answer[0] == "success":
                session['user_id'] = answer[1].id
                session['email'] = email
                session['nickname'] = answer[1].nickname
                return jsonify({
                    'success': True,
                    'redirect_url': '/'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': answer[1]
                }), 401
        else:
            # Также оставил для совместимости
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


@main_bp.route('/logout.html')
def logout():
    session.clear()
    return redirect('/')


# Разделы физика или математика
@main_bp.route('/<subject>_mode.html')
def subject_mode(subject):
    if session.get('user_id') is None:
        return redirect('/login.html')

    if subject not in ['physics', 'math']:
        return redirect('/')
    # Все что с session['completed_task'] это я так понял отладка, ее не трогал
    session['completed_task'] = SolvedProblem.get_solved_problems(session['user_id'])
    page = request.args.get('page', 1, type=int)
    per_page = 10

    problems_query = Problem.query.filter_by(object=subject)
    total = problems_query.count()
    total_pages = (total + per_page - 1) // per_page
    offset = (page - 1) * per_page
    problems = problems_query.offset(offset).limit(per_page).all()

    return render_template(f'{subject}_mode.html',
                           problems=problems,
                           current_page=page,
                           total_pages=total_pages)


# "Карточка" с задачей логику оставил
@main_bp.route("/problem/<int:problem_id>", methods=['GET', 'POST'])
def problem_detail(problem_id):
    if request.method == 'GET':
        problem = Problem.get_problem(id=problem_id)
        return render_template("problem_detail.html",
                               problem=problem,
                               subject=problem.object,
                               task_text=problem.condition,
                               task_image=problem.attachment)

    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            answer = data.get('answer')
        else:
            # Для совместимости
            answer = request.form['answer']

        server_answer = SolvedProblem.add_solved_problem(session.get('user_id'), answer, problem_id)
        if request.is_json:
            if server_answer[0] == "success":
                if 'completed_task' not in session:
                    session['completed_task'] = []
                if str(problem_id) not in session['completed_task']:
                    session['completed_task'].append(str(problem_id))
                session.modified = True
                return jsonify({'success': True, 'message': 'Задача решена!'})
            else:
                return jsonify({'success': False, 'message': 'Ответ неверный!'}), 400
        else:
            # Для совместимости
            if server_answer[0] == "success":
                if 'completed_task' not in session:
                    session['completed_task'] = []
                if str(problem_id) not in session['completed_task']:
                    session['completed_task'].append(str(problem_id))
                session.modified = True
            else:
                session[f"incorrect_answer_{problem_id}"] = True
                session.modified = True

            return redirect(f'/problem/{problem_id}')


# Профиль
@main_bp.route('/profile.html')
def profile():
    if session.get('user_id') is None:
        return redirect('/login.html')
    user = User.query.get(session['user_id'])
    return render_template('profile.html',
                           title="Мой профиль",
                           user=user,
                           main_bp=main_bp)


# раздел pvp
@main_bp.route('/pvp_mode.html')
def pvp_mode():
    if session.get('user_id') is None:
        return redirect('/login.html')
    else:
        return render_template('pvp_mode.html')
