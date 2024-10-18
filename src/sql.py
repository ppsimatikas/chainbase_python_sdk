import time
from typing import Dict, List, Optional, Tuple

import pandas as pd

from src.chainbase_api import ChainbaseAPI

MAP_TYPES = {
    "Int8": "int64",
    "Int32": "int64",
    "Int64": "int64",
    "UInt8": "UInt8",
    "UInt32": "UInt32",
    "UInt64": "UInt64",
    "UInt256": None,
    "Nullable(UInt256)": None,
    "Float32": "Float32",
    "Float64": "Float64",
    "Nullable(Float64)": "Float64",
    "String": "object",
    "Nullable(String)": "object",
    "DateTime": "datetime64[ns]",
    "Nullable(DateTime)": "datetime64[ns]",
    "DateTime64(3)": "datetime64[ns]",
    "Decimal(76, 0)": "Float64",
    "Decimal(38, 0)": "Float64",
    "Array(String)": None,
    "Array(UInt32)": None,
    "Array(UInt256)": None,
    "Array(Array(String))": None,
}


class ChainbaseSQL(ChainbaseAPI):
    """
    Extension of the ChainbaseAPI class, specifically for handling SQL queries
    and returning results either as raw data or as a pandas DataFrame.

    Inherits from ChainbaseAPI and uses its methods for making HTTP requests to
    the Chainbase API.

    Methods:
        query: Executes an SQL query and returns metadata and results.
        query_pandas: Executes an SQL query and returns the results as a pandas DataFrame.
    """

    def __init__(self, api_key: str):
        """
        Initializes the ChainbaseSQL client with the provided API key.

        Args:
            api_key (str): The API key for authenticating with the Chainbase API.
        """
        super().__init__("https://api.chainbase.online/v1/dw/query", api_key, 0)

    def _get_all_pages(
        self, body, results: Optional[List[Dict[str, str]]] = None
    ) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
        """
        Internal method to handle paginated query responses.

        Args:
            body: The query payload.
            results (Optional[List[Dict[str, str]]]): Accumulator for paginated results.

        Returns:
            Tuple containing metadata and a list of result dictionaries.
        """
        results = results if results else []

        res = self.post(body)
        data = res["data"]
        results += data["result"]

        if not data.get("next_page"):
            return data["meta"], results

        time.sleep(1)
        body = {
            "task_id": data.get("task_id"),
            "page": data.get("next_page"),
        }
        return self._get_all_pages(body, results)

    def query(self, sql: str) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
        """
        Executes an SQL query against the Chainbase API.

        Args:
            sql (str): The SQL query to be executed.

        Returns:
            A tuple containing query metadata and results as a list of dictionaries.
        """
        body = {"query": sql}
        return self._get_all_pages(body)

    def query_pandas(self, sql: str) -> pd.DataFrame:
        """
        Executes an SQL query and returns the results as a pandas DataFrame.

        Args:
            sql (str): The SQL query to be executed.

        Returns:
            pandas DataFrame containing the query results.
        """
        metadata, results = self.query(sql)

        types = self._metadata_to_pandas_types(metadata)

        return pd.DataFrame(results, columns=types.keys()).astype(types)

    @staticmethod
    def _metadata_to_pandas_types(metadata: Dict[str, str]):
        """
        Converts query metadata to pandas DataFrame types.

        Args:
            metadata (Dict[str, str]): Metadata about the columns in the query result.

        Returns:
            A dictionary mapping column names to pandas data types.
        """
        return {m["name"]: MAP_TYPES.get(m["type"], None) for m in metadata}
