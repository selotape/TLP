from datetime import datetime
from typing import Optional

from boltons.iterutils import chunked
from flask_sqlalchemy import SQLAlchemy

from TLP.web import app
from TLP.configuration import DB_FILE

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_FILE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def get_parties(size):
    query = User.query.filter_by(_active=True)
    active_users = query.all()
    for user in active_users:
        user._active = False

    return _chunk_users((repr(u) for u in active_users), size)


def _chunk_users(active_users, size):
    chunked_users = chunked(active_users, size)
    if len(chunked_users) <= 1 or chunked_users[-1] == size:
        return chunked_users

    chunked_users, last_chunk = chunked_users[:-1], chunked_users[-1]
    for i, user in enumerate(last_chunk):
        chunked_users[i].append(user)
    return chunked_users


def put_or_update(name: Optional[str], email: str):
    if not name:
        name = email.split('@')[0]

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)
    else:
        user.latest_touched = datetime.now()
        user._active = True


class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), default='noname')
    latest_touched = db.Column(db.Date(), default=datetime.now())
    _active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'({self.name}, {self.email})'


db.create_all()
