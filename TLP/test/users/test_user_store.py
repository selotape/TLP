import string

from TLP.users import UserStore


def test_party_partitioning(user_store: UserStore):
    users = list(string.ascii_lowercase)
    for user in users:
        user_store.put_user(user, user)

    party_size = 4
    parties = list(user_store.get_parties(size=party_size))
    assert len(parties) == len(string.ascii_lowercase) // party_size
    len_parties = [len(party) for party in parties]
    assert sum(len_parties) == len(users)
    assert all(party_size <= len_ <= party_size + 1 for len_ in len_parties)
