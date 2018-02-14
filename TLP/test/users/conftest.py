import pytest

from TLP.users import _UserStore


@pytest.fixture
def user_store():
    return _UserStore()
