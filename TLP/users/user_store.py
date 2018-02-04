from boltons.iterutils import chunked
from sqlalchemy import Column, String, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, Query

_Base = declarative_base()


class UserStore:
    def __init__(self):
        engine = create_engine('sqlite:///:memory:')
        self._sessionmaker = sessionmaker(bind=engine, autocommit=True)
        self._session: Session = self._sessionmaker()
        _Base.metadata.create_all(engine)

    def put_user(self, name, email):
        user = User(name=name, email=email, _active=True)
        self._session.add(user)

    def get_parties(self, size):
        query: Query = self._session.query(User).filter_by(_active=True)
        active_users = query.all()
        for user in active_users:
            user._active = False

        return self._chunk(active_users, size)

    @staticmethod
    def _chunk(active_users, size):
        extra_count = len(active_users) % size
        extra_users = active_users[-extra_count:]
        chunked_users = chunked(active_users[:-extra_count], size)
        for i, user in enumerate(extra_users):
            chunked_users[i].append(user)
        return chunked_users


class User(_Base):
    __tablename__ = 'users'

    email = Column(String(100), primary_key=True)
    name = Column(String(100))
    _active = Column(Boolean)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', active='{self._active}')>"
