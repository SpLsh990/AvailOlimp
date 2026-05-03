from flask import render_template, Blueprint, request, session, redirect, jsonify
from control_data_base import User, Problem, SolvedProblem
import secrets
import requests

# зависимости
main_bp = Blueprint('main_bp', __name__,
                    template_folder='../templates/main',
                    static_folder='../static')

GOOGLE_CLIENT_ID = '922930227873-tnmm1pickre1o6cnm9qf6aunteq7ifro.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'http://localhost:5000/auth/callback' # ПОМЕНЯТЬ НА СТАТИЧЕСКИЙ В ФИНАЛЕ
GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'

# TODO Убрать все что для совместимости

# главный блок (index, register, login, logout)
@main_bp.route('/')
def index():
    if session.get('user_id'):
        print(session.get('user_id'))
        return render_template('index.html',
                               title="AvailOlimp", main_bp=main_bp)
    else:

        session.clear()
        return render_template('index.html',
                               title="AvailOlimp", main_bp=main_bp)


@main_bp.route('/form_register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('form_register.html', title="Register Form", main_bp=main_bp)

    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            nickname = data.get('nickname')

            answer = User.register_user(email, password, nickname, False)

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

            answer = User.register_user(email, password, nickname, False)

            if answer[0] == "success":
                session['user_id'] = answer[1]
                session['email'] = email
                session['nickname'] = nickname
                return redirect('/')
            else:
                session['register_error'] = answer[1]
                return redirect('/form_register')

@main_bp.route('/form_register_google', methods=['GET', 'POST'])
def register_google():
    if request.method == 'GET':
        return render_template('form_register_google.html', title="Register Form", main_bp=main_bp)

    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            print(data)
            email = session['email']
            password = data.get('password')
            nickname = data.get('nickname')
            print(nickname)

            answer = User.register_user(email, password, nickname, True)

            if answer[0] == "success":
                session['user_id'] = answer[1]
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
            email = session['email']
            password = request.form['password']
            nickname = request.form['nickname']

            answer = User.register_user(email, password, nickname, True)

            if answer[0] == "success":
                session['user_id'] = answer[1]
                session['nickname'] = nickname
                return redirect('/')
            else:
                session['register_error'] = answer[1]
                return redirect('/form_register_google')


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title="Login Form", main_bp=main_bp)

    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            answer = User.login_user(email, password, False)
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
            answer = User.login_user(email, password, False)
            if answer[0] == "success":
                session['user_id'] = answer[1].id
                session['email'] = email
                session['nickname'] = answer[1].nickname
                return redirect('/')
            else:
                session['error_password_email'] = True
                return redirect('/login')


def generate_auth_url(auth_url, params):
    return f"{auth_url}?{requests.compat.urlencode(params)}"


@main_bp.route('/google_redirect')
def login_oauth():
    # Начало авторизации через Google
    reg = request.args.get('registration')

    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'email profile' if reg == 'True' else 'email',
        'state': reg,
        'prompt':'consent'
    }

    # Формируем URL для редиректа
    auth_url = generate_auth_url(GOOGLE_AUTH_URL, params)
    return redirect(auth_url)


@main_bp.route('/auth/callback')
def callback():

    # Получаем код авторизации
    code = request.args.get('code')
    if not code:
        print('Ошибка: код авторизации не получен')
        return redirect('/')

    # Обмениваем код на токен
    token_data = {
        'client_id': '922930227873-tnmm1pickre1o6cnm9qf6aunteq7ifro.apps.googleusercontent.com',
        'client_secret': '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',
        'grant_type': 'authorization_code',
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'code': code
    }

    # Запрос на получение токена
    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    if token_response.status_code != 200:
        print('Ошибка получения токена')
        return redirect('/')

    tokens = token_response.json()
    access_token = tokens.get('access_token')

    # Получаем информацию о пользователе
    user_response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={'Authorization': f'Bearer {access_token}'}
    )

    if user_response.status_code != 200:
        return 'Ошибка получения данных пользователя', 400

    user_info = user_response.json()

    # Сохраняем данные пользователя в сессии

    reg = request.args.get('state')
    session['email'] = user_info.get('email')
    try:
        answer = User.login_user(session['email'], None, True)
        session['user_id'] = answer[1].id
        session['nickname'] = answer[1].nickname
    except Exception:
        return redirect('/form_register_google')
    return redirect('/')


@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')


# Разделы физика или математика
@main_bp.route('/<subject>_mode.html')
def subject_mode(subject):
    if session.get('user_id') is None:
        return redirect('/login')

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
@main_bp.route('/profile')
def profile():
    if session.get('user_id') is None:
        return redirect('/login')
    user = User.query.get(session['user_id'])
    return render_template('profile.html',
                           title="Мой профиль",
                           user=user,
                           main_bp=main_bp)


# раздел pvp
@main_bp.route('/pvp_mode')
def pvp_mode():
    if session.get('user_id') is None:
        return redirect('/login')
    else:
        user = User.query.filter_by(nickname=session["nickname"]).first()
        if user.elo == -1:
            User.add_rating(session["nickname"], 1001)
            user = User.query.filter_by(nickname=session["nickname"]).first()
            session["elo"] = user.elo
            print(session["elo"])
            win = user.winner
            lose = user.loser
            winrate = win * 100 / (win + lose) if win + lose != 0 else 0
            return render_template('pvp_mode.html', show_rules=True, elo=session["elo"], winner=win,
                                   loser=lose, winrate=winrate)

        else:
            user = User.query.filter_by(nickname=session["nickname"]).first()
            session["elo"] = user.elo
            print(session["elo"])
            win = user.winner
            lose = user.loser
            winrate = win * 100 / (win + lose) if win + lose != 0 else 0
            return render_template('pvp_mode.html', show_rules=False, elo=session["elo"], winner=win,
                                   loser=lose, winrate=winrate)
