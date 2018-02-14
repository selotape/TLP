from datetime import datetime

from boltons.iterutils import chunked
from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, Query

from TLP.util import Singleton

_Base = declarative_base()


class _UserStore(metaclass=Singleton):
    def __init__(self):
        engine = create_engine('sqlite:///:memory:')
        self._sessionmaker = sessionmaker(bind=engine, autocommit=True)
        self._session: Session = self._sessionmaker()
        _Base.metadata.create_all(engine)

    def put_user(self, name, email):
        self._put_or_update(name, email)

    def get_parties(self, size):
        query: Query = self._session.query(User).filter_by(_active=True)
        active_users = query.all()
        for user in active_users:
            user._active = False

        return self._chunk(active_users, size)

    @staticmethod
    def _chunk(active_users, size):
        chunked_users = chunked(active_users, size)
        if len(chunked_users) <= 1 or chunked_users[-1] == size:
            return chunked_users

        chunked_users, last_chunk = chunked_users[:-1], chunked_users[-1]
        for i, user in enumerate(last_chunk):
            chunked_users[i].append(user)
        return chunked_users

    def _put_or_update(self, name, email):
        user = self._session.query(User).filter_by(email=email).first()
        if not user:
            user = User(email=email, name=name)
            self._session.add(user)
        else:
            user.latest_touched = datetime.now()
            user._active = True


class User(_Base):
    __tablename__ = 'users'

    email = Column(String(100), primary_key=True)
    name = Column(String(100))
    latest_touched = Column(Date(), default=datetime.now())
    _active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', active='{self._active}')>"


user_store = _UserStore()
