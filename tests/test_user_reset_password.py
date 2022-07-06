import pytest

from tests.conftest import init_redis


class TestSuccess:
    @pytest.fixture(autouse=True, scope="class")
    def setup(self):
        init_redis()
