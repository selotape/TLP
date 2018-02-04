import pytest

from TLP.users import UserStore


@pytest.fixture
def user_store():
    return UserStore()
