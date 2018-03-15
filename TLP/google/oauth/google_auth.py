import logging

from flask import Flask, redirect, url_for, session, jsonify
from flask_oauthlib.client import OAuth, OAuthException

from TLP.configuration import LUNCH_TIME, POST_LUNCH_TIME, PARTY_SIZE
from TLP.users import user_store
from TLP.util import day_cache
from TLP.util.time import datetime_in_israel

_log = logging.getLogger(__name__)

try:
    from TLP.google.oauth import google_secrets
except ImportError:
    _log.fatal("No google secrets configuration. See install manual!")
    google_secrets = None
    exit(-1)

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


@app.route('/')
def root():
    time = datetime_in_israel().strftime('%H:%M')
    if LUNCH_TIME < time < POST_LUNCH_TIME:
        return jsonify({"TLP_parties": {i: party for i, party in enumerate(_get_parties(), start=1)},
                        "message": f"Come back again tomorrow before {LUNCH_TIME}!"})
    elif time > POST_LUNCH_TIME:
        return jsonify({'message': f"Sorry, TLP is closed for today. Come back tomorrow before {LUNCH_TIME}!"})
    elif 'google_token' in session:
        return jsonify({'message': f"TLPs team of highly trained monkeys has been dispatched to process your request.\nCome back at {LUNCH_TIME} for results!"})
    else:
        return redirect(url_for('login'))


@day_cache
def _get_parties():
    return user_store.get_parties(size=PARTY_SIZE)


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
        if not session.get('google_token') and 'already redeemed' not in e.data.get('error_description', {}):
            return redirect(url_for('login'))

    user_google_info = google.get('userinfo')
    user_store.put_or_update(None, user_google_info.data['email'])
    _log.info(user_google_info.data)
    return redirect(url_for('root'))


@app.route('/logout')
@app.route('/signout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('login'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
