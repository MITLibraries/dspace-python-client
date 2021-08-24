# dspace/client.py
from typing import Any, Dict, Optional

import requests
import structlog

logger = structlog.get_logger(__name__)


class DSpaceClient:
    """A Client class for interacting with the DSpace REST API.

    Args:
        base_url: The base url of the DSpace API
        accept_header: The response type to use in the requests "accept" header -- one
            of "application/json" or "application/xml", defaults to "application/json"

    Returns:
        :class:`DSpaceClient` object

    Example:
        >>> from dspace.client import DSpaceClient
        >>> client = DSpaceClient("https://dspace.myuniversity.edu/api")
        >>> client.login("user@example.com", "password")
    """

    def __init__(self, base_url: str, accept_header: str = "application/json"):
        self.base_url: str = base_url.rstrip("/")
        self.headers: dict[str] = {"accept": accept_header}
        self.cookies: dict[str] = {}
        logger.debug(
            f"Client initialized with params base_url={self.base_url}, "
            f"accept_header={self.headers}"
        )

    def __repr__(self):
        return (
            f"DSpaceClient(base_url='{self.base_url}', "
            f"accept_header='{self.headers['accept']}')"
        )

    def get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        """Send a GET reqeust to the specified endpoint and return the result.

        Args:
            endpoint: The DSPace REST endpoint to get, e.g. "/status"
            params: Additional params that should be submitted with the request

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.exceptions.HTTPError`: Response status code is 4xx or 5xx
            :class:`requests.exceptions.Timeout`: Server takes more than 5 seconds to
                respond
        """
        url = self.base_url + endpoint
        response = requests.get(
            url, cookies=self.cookies, headers=self.headers, params=params, timeout=5.0
        )
        response.raise_for_status()
        return response

    def login(self, email: str, password: str) -> None:
        """Authenticate a user to the DSpace REST API. If authentication is successful,
        adds an object to `self.cookies` equal to the response 'JSESSIONID' cookie.

        Args:
            email: The email address of the DSpace user
            password: The password of the DSpace user

        Raises:
            :class:`requests.exceptions.HTTPError`: Response status code 401 unauthorized
        """
        logger.debug(f"Attempting to authenticate to {self.base_url} as {email}")
        endpoint = "/login"
        data = {"email": email, "password": password}
        response = self.post(endpoint, data=data)
        self.cookies["JSESSIONID"] = response.cookies.get("JSESSIONID")
        logger.debug(f"Successfully authenticated to {self.base_url} as {email}")

    def post(
        self, endpoint: str, data: Optional[bytes], params: Optional[dict] = None
    ) -> requests.Response:
        """Send a POST request to a specified endpoint and return the result.

        Args:
            endpoint: The DSPace REST endpoint to post to, e.g. "/login"
            data: The data to post
            params: Additional params that should be submitted with the request

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.exceptions.HTTPError`: Response status code 4xx or 5xx
            :class:`requests.exceptions.Timeout`: Server takes more than 5 seconds to
                respond
        """
        url = self.base_url + endpoint
        response = requests.post(
            url,
            cookies=self.cookies,
            data=data,
            headers=self.headers,
            params=params,
            timeout=5.0,
        )
        response.raise_for_status()
        return response

    def status(self) -> Dict[str, Any]:
        """Get current authentication status of :class:`DSpaceClient` instance.

        Returns:
            Dict representation of `DSpace Status object`_

            .. _DSpace Status object: https://wiki.lyrasis.org/display/DSDOC6x/\
                REST+API#RESTAPI-StatusObject
        """
        logger.debug(f"Retrieving authentication status from {self.base_url}")
        endpoint = "/status"
        response = self.get(endpoint)
        return response.json()
