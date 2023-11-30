from typing import Dict

import requests

DEFAULT_ERROR = "An unexpected error occurred while calling the Chainbase API."


class ChainbaseAPI:
    """
    A client for the Chainbase API.

    This class provides methods to interact with the Chainbase API. It handles the
    details of making HTTP requests and processing responses.

    Attributes:
        url (str): The base URL for the Chainbase API.
        headers (dict): HTTP headers to include with requests, including the API key.
    """

    def __init__(self, url: str, api_key: str):
        """
        Initializes the ChainbaseAPI client with the specified API URL and key.

        Args:
            url (str): The base URL for the Chainbase API.
            api_key (str): The API key for authenticating with the Chainbase API.
        """
        self.url = url

        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json; charset=utf-8",
        }

    def post(self, body: any) -> Dict[str, any]:
        """
        Sends a POST request to the Chainbase API with the provided body.

        Args:
            body (Any): The payload to be sent in the POST request.

        Returns:
            Dict[str, Any]: The JSON response from the API.

        Raises:
            Exception: If the API returns an error code or if there's an issue with
                        the response data structure.
        """
        res = requests.post(self.url, json=body, headers=self.headers)
        res.raise_for_status()
        json_res = res.json()

        if json_res.get("code") != 0:
            error = json_res.get("error", DEFAULT_ERROR) or DEFAULT_ERROR
            raise Exception(error)

        data = json_res.get("data")

        if data is None:
            raise Exception(DEFAULT_ERROR)

        if data and data.get("err_msg"):
            raise Exception(data.get("err_msg", DEFAULT_ERROR))

        return json_res
