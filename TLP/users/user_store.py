from datetime import datetime
from typing import Optional

from boltons.iterutils import chunked
from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, Query

from TLP.configuration import *

_Base = declarative_base()

_engine = create_engine(f'sqlite:///{DB_FILE}')
_sessionmaker = sessionmaker(bind=_engine, autocommit=True)
_session: Session = _sessionmaker()


def get_parties(size):
    query: Query = _session.query(User).filter_by(_active=True)
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

    user = _session.query(User).filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        _session.add(user)
    else:
        user.latest_touched = datetime.now()
        user._active = True


class User(_Base):
    __tablename__ = 'users'

    email = Column(String(100), primary_key=True)
    name = Column(String(100), default='noname')
    latest_touched = Column(Date(), default=datetime.now())
    _active = Column(Boolean, default=True)

    def __repr__(self):
        return f'({self.name}, {self.email})'


def bootstrap():
    _Base.metadata.create_all(_engine)


bootstrap()
