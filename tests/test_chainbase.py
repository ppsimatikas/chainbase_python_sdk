import os
import unittest

from chainbase_sdk.chainbase import MISSING_API_KEY_ERROR, Chainbase
from chainbase_sdk.sql import ChainbaseSQL


class TestChainbase(unittest.TestCase):
    def test_init(self):
        self.client = Chainbase("api-key")

        assert isinstance(self.client.sql, ChainbaseSQL)

    def test_init_env_key(self):
        os.environ["CHAINBASE_API_KEY"] = "api-key"
        self.client = Chainbase()

        assert isinstance(self.client.sql, ChainbaseSQL)

    def test_init_no_keys(self):
        os.environ["CHAINBASE_API_KEY"] = ""

        with self.assertRaises(ValueError) as err:
            self.client = Chainbase()

        assert MISSING_API_KEY_ERROR in str(err.exception)
