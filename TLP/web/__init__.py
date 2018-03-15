from flask import Flask

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'

from TLP.web import views
