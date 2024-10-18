import os
from typing import Optional

from chainbase_sdk.sql import ChainbaseSQL
from chainbase_sdk.sql_alpha import ChainbaseSQLAlpha

MISSING_API_KEY_ERROR = """

Please provide a Chainbase API key, or set the `CHAINBASE_API_KEY` environment variable.
Follow the steps below to obtain your API key:
1. Go to: https://console.chainbase.com/
2. Under `Dashboard`
3. Select existing project or `New Project`
4. Copy the `API Key`.
"""


class Chainbase:
    """
    A client for interacting with the Chainbase API. https://docs.chainbase.com/docs

    This client provides an interface to perform operations using the Chainbase API.
    It requires an API key for authentication, which can be provided either directly
    or through an environment variable.

    Attributes:
        sql: An instance of ChainbaseSQL for executing SQL queries.
             Details here: https://docs.chainbase.com/reference/data-cloud-sql

    Raises:
        ValueError: If the API key is not provided either as a parameter or
                    through the environment variable 'CHAINBASE_API_KEY'.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the Chainbase client with the provided API key.

        Args:
            api_key: The API key for authenticating with the Chainbase API.
                     If not provided, the API key is obtained from the
                     'CHAINBASE_API_KEY' environment variable.

        Raises:
            ValueError: If the API key is not provided either directly or through the
                        environment variable.
        """
        api_key = api_key if api_key else os.environ.get("CHAINBASE_API_KEY")

        if not api_key:
            raise ValueError(MISSING_API_KEY_ERROR)

        self.sql = ChainbaseSQL(api_key)
        self.sql_alpha = ChainbaseSQLAlpha(api_key)
