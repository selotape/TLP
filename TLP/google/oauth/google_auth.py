import logging

_log = logging.getLogger(__name__)
try:
    from TLP.google.oauth import google_secrets
except ImportError:
    _log.fatal("No google secrets configuration. See install manual!")
    google_secrets = None
    exit(-1)

from flask import session
from flask_oauthlib.client import OAuth

from TLP.web import app

app.config['GOOGLE_ID'] = google_secrets.CLIENT_ID
app.config['GOOGLE_SECRET'] = google_secrets.CLIENT_SECRET
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


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
