from flask import Flask, render_template, Blueprint, request

main_bp = Blueprint('main_bp', __name__,
                    template_folder='../templates/main',
                    static_folder='../static')

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
        print(email, password)
        return """
        <h1>Status: OK</h1>
        """