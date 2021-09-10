# dspace/client.py
"""DSpace client module.

This module includes a Client class for interacting with the DSpace REST API.
"""
import logging
from typing import Dict, Optional, Union

import requests

logger = logging.getLogger(__name__)


class DSpaceClient:
    """A Client class for interacting with the DSpace REST API.

    Args:
        base_url: The base url of the DSpace API
        accept_header: The response type to use in the requests "accept" header -- one
            of "application/json" or "application/xml", defaults to "application/json"

    Attributes:
        base_url: The base url of the DSpace API
        cookies: Cookies for use in client requests
        headers: Headers for use in client requests
    """

    def __init__(self, base_url: str, accept_header: str = "application/json"):
        self.base_url: str = base_url.rstrip("/")
        self.headers: Dict[str, str] = {"accept": accept_header}
        self.cookies: dict = {}
        logger.debug(
            f"Client initialized with params base_url={self.base_url}, "
            f"accept_header={self.headers}"
        )

    def __repr__(self):
        return (
            f"DSpaceClient(base_url='{self.base_url}', "
            f"accept_header='{self.headers['accept']}')"
        )

    def delete(self, endpoint: str) -> requests.Response:
        """Send a DELETE request to the specified endpoint and return the result.

        This method is internal to the library (although not private to this class)
        and should generally not be called directly. It is used by other classes to send
        DELETE requests using the client's stored authentication cookie and headers.

        Args:
            endpoint: The DSPace REST endpoint for object to delete, e.g. "/items/abc123"

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.exceptions.HTTPError`: if response status code is 4xx or
                5xx
            :class:`requests.exceptions.Timeout`: if server takes more than 5 seconds to
                respond
        """
        url = self.base_url + endpoint
        response = requests.delete(
            url, cookies=self.cookies, headers=self.headers, timeout=5.0
        )
        response.raise_for_status()
        return response

    def get(self, endpoint: str, params: Optional[dict] = None) -> requests.Response:
        """Send a GET request to the specified endpoint and return the result.

        This method is internal to the library (although not private to this class)
        and should generally not be called directly. It is used by other classes to send
        GET requests using the client's stored authentication cookie and headers.

        Args:
            endpoint: The DSPace REST endpoint to get, e.g. "/status"
            params: Additional params that should be submitted with the request

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.exceptions.HTTPError`: if response status code is 4xx or
                5xx
            :class:`requests.exceptions.Timeout`: if server takes more than 5 seconds to
                respond
        """
        url = self.base_url + endpoint
        response = requests.get(
            url, cookies=self.cookies, headers=self.headers, params=params, timeout=5.0
        )
        response.raise_for_status()
        return response

    def get_object_by_handle(self, handle: str) -> requests.Response:
        """Get a DSpace object based on its handle instead of its UUID.

        Args:
            handle: Handle of a DSpace community, collection, or item, e.g.
                '1721.1/130883'

        Returns:
            :class:`requests.Response` object.
            Response body is a json representation of the DSpace object with the
            provided handle

        Raises:
            :class:`requests.HTTPError`: 500 Server Error if no object matching the
                provided handle is found
        """
        logger.debug(f"Retrieving object by handle {handle}")
        endpoint = f"/handle/{handle}"
        response = self.get(endpoint)
        return response

    def login(self, email: str, password: str) -> None:
        """Authenticate a user to the DSpace REST API.

        If authentication is successful, adds an object to `self.cookies` equal to the
        response 'JSESSIONID' cookie.

        Args:
            email: The email address of the DSpace user
            password: The password of the DSpace user

        Raises:
            :class:`requests.exceptions.HTTPError`: 401 Client Error if provided
                credentials are unauthorized
        """
        logger.debug(f"Attempting to authenticate to {self.base_url} as {email}")
        endpoint = "/login"
        data = {"email": email, "password": password}
        response = self.post(endpoint, data=data)
        self.cookies["JSESSIONID"] = response.cookies.get("JSESSIONID")
        logger.debug(f"Successfully authenticated to {self.base_url} as {email}")

    def post(
        self,
        endpoint: str,
        data: Optional[Union[bytes, dict]] = None,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> requests.Response:
        """Send a POST request to a specified endpoint and return the result.

        This method is internal to the library (although not private to this class)
        and should generally not be called directly. It is used by other classes to send
        POST requests using the client's stored authentication cookie and headers.

        Args:
            endpoint: The DSPace REST endpoint to post to, e.g. "/login"
            data: The data to post
            json: Data to post as JSON (uses requests' built-in JSON encoder)
            params: Additional params that should be submitted with the request

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.exceptions.HTTPError`: if response status code is 4xx or
                5xx
            :class:`requests.exceptions.Timeout`: if server takes more than 15 seconds
                to respond
        """
        url = self.base_url + endpoint
        response = requests.post(
            url,
            cookies=self.cookies,
            data=data,
            headers=self.headers,
            json=json,
            params=params,
            timeout=15.0,
        )
        response.raise_for_status()
        return response

    def status(self) -> requests.Response:
        """Get current authentication status of :class:`DSpaceClient` instance.

        Returns:
            :class:`requests.Response` object.
            Response body is a json representation of a `DSpace Status object`_

            .. _DSpace Status object: https://wiki.lyrasis.org/display/DSDOC6x/\
                REST+API#RESTAPI-StatusObject
        """
        logger.debug(f"Retrieving authentication status from {self.base_url}")
        endpoint = "/status"
        response = self.get(endpoint)
        return response
