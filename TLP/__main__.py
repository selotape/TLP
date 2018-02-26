from logging.config import fileConfig as loggingFileConfig

from TLP.google.oauth.google_auth import app

LOGGING_CONFIG = './logging_config.ini'

if __name__ == '__main__':
    try:
        loggingFileConfig(LOGGING_CONFIG)
    except KeyError as e:
        print(f"Couldn't locate the {LOGGING_CONFIG} file")
    app.run(debug=True)