import logging

from flask import Flask, redirect, url_for, session, jsonify
from flask_oauthlib.client import OAuth, OAuthException

from TLP.google.oauth import google_secrets
from TLP.users import user_store
from TLP.util import datetime_in_israel, day_cache, seconds_till_eleven_thirty

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
def root():
    time = datetime_in_israel().strftime('%H%M')
    if time < '1130' or 'google_token' not in session:
        return redirect(url_for('login'))
    else:
        return jsonify({"today\'s_parties": {i: party for i, party in enumerate(_get_parties(), start=1)}})


@day_cache
def _get_parties():
    return user_store.get_parties(size=4)


@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/login/authorized')
def authorized():
    time = datetime_in_israel().strftime('%H%M')
    if time > '1130':
        return jsonify({'message': f"Sorry, we're closed for today. Please come back tomorrow!"})

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
    log.info(user_google_info.data)
    return jsonify({'message': f"You're in! Come back in {seconds_till_eleven_thirty()} seconds to check out results."})


@app.route('/logout')
@app.route('/signout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('login'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
