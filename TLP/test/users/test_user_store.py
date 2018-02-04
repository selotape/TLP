import string


def test_party_partitioning(user_store):
    users = list(string.ascii_lowercase)
    for user in users:
        user_store.put(user)

    party_size = 4
    parties = list(user_store.get_parties(size=party_size))
    assert len(parties) == string.ascii_lowercase // party_size
    assert all(len(party) == party_size for party in parties[:-1])
    assert len(parties[-1] == party_size + len(users) % party_size)
