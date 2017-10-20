from flask import Flask, render_template, json, request
from werkzeug.security import generate_password_hash  # , check_password_hash

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/showSignUp')
def show_sign_up():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def sign_up():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _hashed_password = generate_password_hash(_password)

    # validate the received values
    if _name and _email and _hashed_password:
        return json.dumps({'html': '<span>All fields good !!</span>'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})


if __name__ == '__main__':
    app.run()
