import unittest
from unittest.mock import call, patch

import pandas as pd
from pandas.testing import assert_frame_equal

from chainbase_sdk.sql import ChainbaseSQL


@patch("src.sql.ChainbaseAPI.post")
class TestSQL(unittest.TestCase):
    def setUp(self):
        self.url = "https://api.chainbase.online/v1/dw/query"
        self.query = "select * from test"
        self.chainbaseSQL = ChainbaseSQL("api-key")

    def test_query(self, post_mock):
        post_mock.return_value = {"data": {"meta": "metadata", "result": ["r1"]}}

        meta, results = self.chainbaseSQL.query(self.query)

        post_mock.assert_called_with({"query": self.query})

        self.assertEqual(meta, "metadata")
        self.assertEqual(results, ["r1"])

    def test_query_many_pages(self, post_mock):
        post_mock.side_effect = [
            {
                "data": {
                    "meta": "metadata",
                    "result": ["r1"],
                    "next_page": 2,
                    "task_id": "task_id",
                }
            },
            {"data": {"meta": "metadata", "result": ["r2"]}},
        ]

        meta, results = self.chainbaseSQL.query(self.query)

        post_mock.assert_has_calls(
            [
                call({"query": self.query}),
                call(
                    {
                        "task_id": "task_id",
                        "page": 2,
                    }
                ),
            ]
        )

        self.assertEqual(meta, "metadata")
        self.assertEqual(results, ["r1", "r2"])

    def test_query_pandas(self, post_mock):
        metadata = [
            {"name": "column1", "type": "String"},
            {"name": "column2", "type": "Decimal(76, 0)"},
        ]

        result = [
            {"column1": "k11", "column2": 2.1},
            {"column1": "k12", "column2": 2.2},
        ]

        post_mock.return_value = {"data": {"meta": metadata, "result": result}}

        df = self.chainbaseSQL.query_pandas(self.query)

        post_mock.assert_called_with({"query": self.query})

        expected = pd.DataFrame(result).astype(
            {"column1": "object", "column2": "Float64"}
        )
        assert_frame_equal(df, expected)

    def test_query_pandas_many_pages(self, post_mock):
        metadata = [
            {"name": "column1", "type": "String"},
            {"name": "column2", "type": "Decimal(76, 0)"},
        ]

        result1 = [
            {"column1": "k11", "column2": 2.1},
            {"column1": "k12", "column2": 2.2},
        ]

        result2 = [
            {"column1": "k211", "column2": 22.1},
            {"column1": "k212", "column2": 22.2},
        ]

        post_mock.side_effect = [
            {
                "data": {
                    "meta": metadata,
                    "result": result1,
                    "next_page": 2,
                    "task_id": "task_id",
                }
            },
            {"data": {"meta": metadata, "result": result2}},
        ]

        df = self.chainbaseSQL.query_pandas(self.query)

        post_mock.assert_has_calls(
            [
                call({"query": self.query}),
                call(
                    {
                        "task_id": "task_id",
                        "page": 2,
                    }
                ),
            ]
        )

        expected = pd.DataFrame(result1 + result2).astype(
            {"column1": "object", "column2": "Float64"}
        )
        assert_frame_equal(df, expected)
