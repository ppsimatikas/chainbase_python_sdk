import unittest

import requests
import requests_mock

from chainbase_sdk.chainbase_api import DEFAULT_ERROR, ChainbaseAPI


@requests_mock.mock()
class TestChainbaseAPI(unittest.TestCase):
    def setUp(self):
        self.url = "http://api.example.com"
        self.body = {"query": "test"}
        self.api = ChainbaseAPI(self.url, "api-key")

    def test_post_success(self, requests_mock_obj):
        response_body = {"code": 0, "data": {"meta": {}}}
        requests_mock_obj.post(self.url, json=response_body)

        response = self.api.post(self.body)
        self.assertEqual(response, {"code": 0, "data": {"meta": {}}})

    def test_post_error_code(self, requests_mock_obj):
        response_body = {"code": 1, "error": "error"}
        requests_mock_obj.post(self.url, json=response_body)

        with self.assertRaises(Exception) as err:
            self.api.post(self.body)

        assert "error" in str(err.exception)

        response_body = {"code": 1, "error": None}
        requests_mock_obj.post(self.url, json=response_body)

        with self.assertRaises(Exception) as err:
            self.api.post(self.body)

        assert DEFAULT_ERROR in str(err.exception)

        response_body = {"code": 1}
        requests_mock_obj.post(self.url, json=response_body)

        with self.assertRaises(Exception) as err:
            self.api.post(self.body)

        assert DEFAULT_ERROR in str(err.exception)

    def test_post_no_data(self, requests_mock_obj):
        response_body = {"code": 0, "data": None}
        requests_mock_obj.post(self.url, json=response_body)

        with self.assertRaises(Exception) as err:
            self.api.post(self.body)

        assert DEFAULT_ERROR in str(err.exception)

    def test_post_err_msg(self, requests_mock_obj):
        response_body = {"code": 0, "data": {"err_msg": "error"}}
        requests_mock_obj.post(self.url, json=response_body)

        with self.assertRaises(Exception) as err:
            self.api.post(self.body)

        assert "error" in str(err.exception)

    def test_post_http_error(self, requests_mock_obj):
        requests_mock_obj.post(self.url, status_code=404)

        with self.assertRaises(requests.exceptions.HTTPError) as err:
            self.api.post(self.body)

        assert "404 Client Error: None for url: http://api.example.com/" in str(
            err.exception
        )
