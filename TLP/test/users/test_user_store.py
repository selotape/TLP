import string

from TLP.users import _UserStore


def test_party_partitioning(user_store: _UserStore):
    users = list(string.ascii_lowercase)
    for user in users:
        user_store.put_user(user, user)

    party_size = 4
    parties = user_store.get_parties(size=party_size)
    assert len(parties) == len(string.ascii_lowercase) // party_size
    len_parties = [len(party) for party in parties]
    assert sum(len_parties) == len(users)
    assert all(party_size <= len_ <= party_size + 1 for len_ in len_parties)


def test_add_same_user_twice(user_store: _UserStore):
    user_store.put_user('ron', 'vis')
    user_store.put_user('ron', 'vis')
    user_store.put_user('ron', 'vis')

    parties = user_store.get_parties(size=3)
    assert len(parties) == 1
    assert len(parties[0]) == 1


def test_user_store_removes_usedup_users(user_store: _UserStore):
    users = list(string.ascii_lowercase)
    for user in users:
        user_store.put_user(user, user)
    party_size = 4
    active_parties = user_store.get_parties(size=party_size)
    assert len(active_parties) != 0

    inactive_parties = user_store.get_parties(size=party_size)
    assert len(inactive_parties) == 0
