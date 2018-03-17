from logging.config import fileConfig

from TLP.configuration import FLASK_PORT, DB_URI, APP_HOST, DEBUG
from TLP.users.user_store import init_db
from TLP.web import app

LOGGING_CONFIG = './logging_config.ini'

if __name__ == '__main__':
    try:
        fileConfig(LOGGING_CONFIG)
    except KeyError as e:
        print(f"Couldn't locate the {LOGGING_CONFIG} file")
    init_db(app, DB_URI)
    app.run(host=APP_HOST, port=FLASK_PORT, debug=DEBUG)
