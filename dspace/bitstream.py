# dspace/bitstream.py
"""DSpace bitstream module.

This module includes a Bitstream class representing DSpace Bitstream objects, along
with functions for interacting with the DSpace REST API "/bitstreams" endpoint.
"""
import logging
from typing import Optional

import smart_open

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
        bundleName(Optional[str]): The name of the DSpace bundle of the bitstream
        checkSum (Optional[dict[str:str]]): The DSpace-calculated checksum for the
            bitstream, e.g. {"value":"62778292a3a6dccbe2662a2bfca3b86e",
            "checkSumAlgorithm":"MD5"}
        description (Optional[str]): Description of the bitstream
        format (Optional[str]): The DSpace-identified file format of the bitstream
        expand (List[str]: The expand options for the DSpace REST object
        file_path (Optional[str]): File path to the bitstream. Required to post
            bitstream to DSpace. Not part of the DSpace object model, but necessary to
            associate a file with the bitstream
        link (Optional[str]): The DSpace REST API path for the bitstream
        mimeType (Optional[str]): The DSpace-identified mimetype of the bitstream
        name (Optional[str]): The name of the bitstream in DSpace
        parentObject (Optional[str]): Parent object of the bitstream in DSpace
        policies (Optional[list]): Resource policies applied to the bitstream
        retrieveLink (Optional[str]): The DSpace REST API path to directly retrieve the
            bitstream file
        sequenceId (Optional[int]): The DSpace bitstream sequence ID
        sizeBytes (Optional[int]): The DSpace-identified size of the bitstream in bytes
        type (Optional[str]): The DSpace object type
        uuid (Optional[str]): UUID of the bitstream in DSpace
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

        self.bundleName = None
        self.checkSum = None
        self.format = None
        self.expand = ["parent", "policies", "all"]
        self.link = None
        self.mimeType = None
        self.parentObject = None
        self.policies = None
        self.retrieveLink = None
        self.sequenceId = None
        self.sizeBytes = None
        self.type = "bitstream"
        self.uuid = None

    def delete(
        self,
        client: DSpaceClient,
    ) -> None:
        """Delete bitstream from DSpace and unset relevant bitstream attributes.

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class

        Raises:
            :class:`requests.HTTPError`: 404 Not Found if no bitstream matching
                provided UUID
        """
        logger.debug(
            "Deleting bitstream with uuid %s from %s", self.uuid, client.base_url
        )
        response = client.delete(f"/bitstreams/{self.uuid}")
        logger.debug("Delete response: %s", response)
        self.bundleName = None
        self.checkSum = None
        self.format = None
        self.link = None
        self.mimeType = None
        self.parentObject = None
        self.policies = None
        self.retrieveLink = None
        self.sequenceId = None
        self.sizeBytes = None
        self.uuid = None

    def post(
        self,
        client: DSpaceClient,
        item_handle: Optional[str] = None,
        item_uuid: Optional[str] = None,
    ) -> None:
        """Post bitstream to an item and set bitstream attributes to response object values.

        Requires either the `item_handle` or the `item_uuid`, but not both. If
        both are passed, defaults to using the UUID.

        The `smart_open library <https://pypi.org/project/smart-open/>`_ replaces the
        standard open function to stream local or remote files for the POST request.

        Note: DSpace internally uses the file extension from the provided "name"
        parameter (the `bitstream.name` attribute) to assign a format and mimeType when
        creating a new bitstream via API post. If a name with a file extension (e.g.,
        "test-file.pdf") is not provided, DSpace will assign a format of "Unknown" and
        a mimeType of "application/octet-stream".

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class
            item_handle: The handle of an existing item in DSpace to post the bitstream
                to
            item_uuid: The UUID of an existing item in DSpace to post the bitstream to

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
        logger.debug(
            "Posting new bitstream to %s with info %s",
            client.base_url + endpoint,
            params,
        )
        response = client.post(endpoint, data=data, params=params).json()
        logger.debug("Post response: %s", response)
        self.bundleName = response["bundleName"]
        self.checkSum = response["checkSum"]
        self.format = response["format"]
        self.link = response["link"]
        self.mimeType = response["mimeType"]
        self.parentObject = response["parentObject"]
        self.policies = response["policies"]
        self.retrieveLink = response["retrieveLink"]
        self.sequenceId = response["sequenceId"]
        self.sizeBytes = response["sizeBytes"]
        self.uuid = response["uuid"]
