from flask_sqlalchemy import SQLAlchemy

from TLP.util import polite_chunk
from TLP.util.time import today

db = SQLAlchemy()


def get_parties(size):
    todays_users = User.query.filter_by(visit_date=today()).all()
    return polite_chunk((repr(u) for u in todays_users), size)


def register_user(name: str, email: str):
    user = User.query.filter_by(email=email, visit_date=today()).first()
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)


class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    visit_date = db.Column(db.Date(), default=today(), primary_key=True)

    def __repr__(self):
        return f'({self.name}, {self.email})'


def init_db(app, db_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.app = app
    db.init_app(app)
    db.create_all()


def clear_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clearing table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
