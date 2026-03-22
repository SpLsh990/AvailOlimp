from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'test-secret-key-12345'

@app.route('/')
def index():
    session['test'] = 'hello'
    return 'Session is working!'

@app.route('/check')
def check_session():
    if 'test' in session:
        return f'Session value: {session["test"]}'
    else:
        return 'Session is empty'

if __name__ == '__main__':
    print("Secret key:", app.secret_key)
    app.run(debug=True, port=5001)
