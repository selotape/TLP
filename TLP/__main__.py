from logging.config import fileConfig as loggingFileConfig

from TLP.google.oauth.google_auth import app

if __name__ == '__main__':
    loggingFileConfig('./logging_config.ini')
    app.run()
