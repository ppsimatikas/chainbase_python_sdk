import pytest

from src.chainbase import Chainbase
from tests.e2e.tables import tables


@pytest.mark.parametrize("table", tables)
def test_sql(table):
    client = Chainbase()

    query = "select * from %s limit 1001" % table

    metadata, results = client.sql.query(query)
    assert metadata is not None
    assert results is not None

    df = client.sql.query_pandas(query)
    assert df is not None
