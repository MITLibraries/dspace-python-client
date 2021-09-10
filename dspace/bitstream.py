# dspace/bitstream.py
"""DSpace bitstream module.

This module includes a Bitstream class representing DSpace Bitstream objects, along
with functions for interacting with the DSpace REST API "/bitstreams" endpoint.
"""
import logging
from typing import Optional

import smart_open
from requests import Response

from dspace.client import DSpaceClient
from dspace.errors import MissingFilePathError
from dspace.utils import select_identifier

logger = logging.getLogger(__name__)


class Bitstream:
    """Class representing a DSpace Bitstream object and its associated API calls.

    Args:
        description: Description of the bitstream
        file_path: File path to the bitstream. Required to post bitstream to DSpace
        name: Name of the Bitstream

    Attributes:
        description (str): Description of the bitstream
        file_path (str): File path to the bitstream. Required to post bitstream to DSpace
        name (str): Name of the Bitstream
    """

    def __init__(
        self,
        description: Optional[str] = None,
        file_path: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.description = description
        self.file_path = file_path
        self.name = name

    def delete(
        self,
        client: DSpaceClient,
        bitstream_uuid: str,
    ) -> Response:
        """Delete bitstream and return the response.

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.HTTPError`: 404 Not Found if no bitstream matching
                provided UUID
        """
        return client.delete(f"/bitstreams/{bitstream_uuid}")

    def post(
        self,
        client: DSpaceClient,
        item_handle: Optional[str] = None,
        item_uuid: Optional[str] = None,
    ) -> Response:
        """Post bitstream to an item and return the response.

        Requires either the `item_handle` or the `item_uuid`, but not both. If
        both are passed, defaults to using the UUID.

        The `smart_open library <https://pypi.org/project/smart-open/>`_ replaces the
        standard open function to stream local or remote files for the POST request.

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class
            item_handle: The handle of an existing item in DSpace to post the bitstream
                to
            item_uuid: The UUID of an existing item in DSpace to post the bitstream to

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.HTTPError`: 404 Not Found if no item matching
                provided handle/UUID
            MissingFilePathError: if `file_path` attribute is not set on Bitstream
                instance
            MissingIdentifierError: if neither `item_handle` nor `item_uuid`
                parameter is provided
        """
        if not self.file_path:
            raise MissingFilePathError(f"bitstream.post({client}, {item_uuid})")
        item_id = select_identifier(client, item_handle, item_uuid)
        endpoint = f"/items/{item_id}/bitstreams"
        params = {"name": self.name, "description": self.description}
        data = smart_open.open(self.file_path, "rb")
        return client.post(endpoint, data=data, params=params)
