from flask import Flask


def create_app():
    application = Flask(__name__)
    application.debug = True
    application.secret_key = 'development'
    return application


app = create_app()
from TLP.web import views
