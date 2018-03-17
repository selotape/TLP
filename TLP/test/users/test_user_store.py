import string

import pytest
from flask import Flask

from TLP.users import user_store


@pytest.fixture(scope='session', autouse=True)
def create_db():
    user_store.init_db(Flask(__name__), 'sqlite:///:memory:')


@pytest.fixture(autouse=True)
def truncate_users():
    user_store.clear_db()


def test_party_partitioning():
    users = list(string.ascii_lowercase)
    for user in users:
        user_store.register_user(user, user)

    party_size = 4
    parties = user_store.get_parties(size=party_size)
    assert len(parties) == len(string.ascii_lowercase) // party_size
    len_parties = [len(party) for party in parties]
    assert sum(len_parties) == len(users)
    assert all(party_size <= len_ <= party_size + 1 for len_ in len_parties)


def test_add_same_user_twice():
    user_store.register_user('ron', 'vis')
    user_store.register_user('ron', 'vis')
    user_store.register_user('ron', 'vis')

    parties = user_store.get_parties(size=3)
    assert len(parties) == 1
    assert len(parties[0]) == 1
