import logging
import random
from io import StringIO
from pprint import pprint

from flask import Flask, redirect, url_for, session
from flask_oauthlib.client import OAuth, OAuthException

from TLP.google.oauth import google_secrets
from TLP.users import user_store

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

log = logging.getLogger(__name__)


@app.route('/')
@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/login/authorized')
def authorized():
    try:
        resp = google.authorized_response()
        if resp is None:
            return redirect(url_for('login'))
        session['google_token'] = (resp['access_token'], '')
    except OAuthException as e:
        if 'already redeemed' not in e.data['error_description']:
            return redirect(url_for('login'))

    user_google_info = google.get('userinfo')
    user_store.put_user("noname", user_google_info.data['email'])
    log.info(user_google_info.data)
    return '<span>{}</span>'.format(random.choice(signed_in_messages))


@app.route('/get_parties')
def get_parties():
    if 'google_token' not in session:
        return redirect(url_for('login'))
    parties = user_store.get_parties(4)
    formatted_parties = StringIO()
    pprint(parties, stream=formatted_parties)
    return '<span>parties: <text>{}</text></span>'.format(str(parties))


@app.route('/logout')
@app.route('/signout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('login'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
