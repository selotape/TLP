import logging

from flask import jsonify, session, redirect, url_for
from flask_oauthlib.client import OAuthException

from TLP.configuration import LUNCH_TIME, POST_LUNCH_TIME, PARTY_SIZE
from TLP.google.oauth.google_auth import google
from TLP.users import user_store
from TLP.util import day_cache
from TLP.util.time import datetime_in_israel
from TLP.web import app

_log = logging.getLogger(__name__)


@app.route('/')
def root():
    time = datetime_in_israel().strftime('%H:%M')
    if LUNCH_TIME < time < POST_LUNCH_TIME:
        return jsonify({"TLP_parties": _get_parties(),
                        "message": f"Come back again tomorrow before {LUNCH_TIME}!"})
    elif time > POST_LUNCH_TIME:
        return jsonify({'message': f"Sorry, TLP is closed for today. Come back tomorrow before {LUNCH_TIME}!"})
    elif 'google_token' in session:
        return jsonify({'message': f"We've dispatched a team of highly trained monkeys to process your request. Come back at {LUNCH_TIME} for results!"})
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
    email = user_google_info.data['email']
    name = email.split('@')[0]
    user_store.register_user(name, email)
    _log.info(f'Registered user: {user_google_info.data}')
    return redirect(url_for('root'))

# logout is currently not supported
# @app.route('/logout')
# @app.route('/signout')
# def logout():
#     session.pop('google_token', None)
#     # TODO - remove from users_db and replace redirect with a simple message
#     return redirect(url_for('login'))
