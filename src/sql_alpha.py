import time
from typing import Dict, List, Tuple

import pandas as pd

from src.chainbase_api import ChainbaseAPI

MAP_TYPES = {
    "bigint": "int64",
    "varchar": "object",
    "timestamp": "datetime64[ns]",
    "integer": "object",
}


class ChainbaseSQLAlpha(ChainbaseAPI):
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
        super().__init__("https://api.chainbase.com/api/v1/query/execute", api_key, 200)

    def _execute(self, sql: str) -> str:
        """
        Internal method to initiate a query execution

        Args:
            sql: The query sql to execute.

        Returns:
            The execution id
        """
        return self.post({"sql": sql})["data"][0]["executionId"]

    def _check_status(self, execution_id: str) -> str:
        """
        Internal method to check the status of a query execution

        Args:
            execution_id: The query execution id.

        Returns:
            True if it is done, False if it is not
        """
        url = f"https://api.chainbase.com/api/v1/execution/{execution_id}/status"
        data = self.get(url)["data"][0]
        status = data["status"]

        if status == "FAILED":
            raise Exception(data["message"])

        return status == "FINISHED"

    def _get_results(self, execution_id: str) -> str:
        """
        Internal method to check the status of a query execution

        Args:
            execution_id: The query execution id.

        Returns:
             A tuple containing query metadata and results as a list of dictionaries.
        """
        url = f"https://api.chainbase.com/api/v1/execution/{execution_id}/results"
        res = self.get(url)["data"]
        return res["columns"], res["data"]

    def query(self, sql: str) -> Tuple[Dict[str, str], List[Dict[str, str]]]:
        """
        Executes an SQL query against the Chainbase API.

        Args:
            sql (str): The SQL query to be executed.

        Returns:
            A tuple containing query metadata and results as a list of dictionaries.
        """
        execution_id = self._execute(sql)

        max_status_checks = 10
        i = 0
        while i < max_status_checks:
            if self._check_status(execution_id):
                break
            else:
                time.sleep(1)
            i += 1

        if i >= max_status_checks:
            raise Exception("Max retries reached.")

        return self._get_results(execution_id)

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

        # return pd.DataFrame(results, columns=types.keys()).astype(types)
        return pd.DataFrame(results, columns=types.keys())

    @staticmethod
    def _metadata_to_pandas_types(metadata: Dict[str, str]):
        """
        Converts query metadata to pandas DataFrame types.

        Args:
            metadata (Dict[str, str]): Metadata about the columns in the query result.

        Returns:
            A dictionary mapping column names to pandas data types.
        """
        return {
            m["name"]: MAP_TYPES.get(ChainbaseSQLAlpha._get_type(m["type"]), None)
            for m in metadata
        }

    @staticmethod
    def _get_type(t: str):
        if t.startswith("varchar"):
            return "varchar"

        if t not in MAP_TYPES:
            print("NOT EXISTS: ", t)

        return t
