import random

from flask import Flask, redirect, url_for, session, jsonify
from flask_oauthlib.client import OAuth

from TLP.google.oauth import google_secrets

app = Flask(__name__)
app.config['GOOGLE_ID'] = google_secrets.CLIENT_ID
app.config['GOOGLE_SECRET'] = google_secrets.CLIENT_SECRET
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

unauthorized_error_messages = ['WTF you doing here??']
signed_in_messages = ['All done. Now run along.']


@app.route('/')
def index():
    if 'google_token' in session:
        me = google.get('userinfo')
        return jsonify({"data": me.data})
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return '<span>{}</span>'.format(random.choice(unauthorized_error_messages))
    session['google_token'] = (resp['access_token'], '')
    user_google_info = google.get('userinfo')
    print(user_google_info.data)
    return '<span>{}</span>'.format(random.choice(signed_in_messages))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


if __name__ == '__main__':
    app.run()
