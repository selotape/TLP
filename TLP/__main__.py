from logging.config import fileConfig

from TLP.configuration import FLASK_PORT
from TLP.google.oauth.google_auth import app

LOGGING_CONFIG = './logging_config.ini'

if __name__ == '__main__':
    try:
        fileConfig(LOGGING_CONFIG)
    except KeyError as e:
        print(f"Couldn't locate the {LOGGING_CONFIG} file")
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=True)
