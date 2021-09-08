# dspace/item.py
"""DSpace item module.

This module includes classes representing DSpace Item and MetadataEntry objects, along
with functions for interacting with the DSpace REST API "/items" endpoint.
"""

from __future__ import annotations

from typing import Dict, List, Optional

import structlog
from requests import Response

from dspace.bitstream import Bitstream
from dspace.client import DSpaceClient
from dspace.utils import select_identifier

logger = structlog.get_logger(__name__)


class Item:
    """Class representing a DSpace Item object and its associated API calls.

    Args:
        bitstreams: :class:`Bitstream` objects to associate with the item
        metadata: :class:`MetadataEntry` objects to associate with the item

    Attributes:
        bitstreams (list): List of :class:`Bitstream` objects belonging to the item
        metadata (list of :obj:`MetadataEntry`): List of
            :class:`MetadataEntry` objects representing the item's metadata

    """

    def __init__(
        self,
        bitstreams: Optional[List[Bitstream]] = None,
        metadata: Optional[List[MetadataEntry]] = None,
    ):
        self.bitstreams = bitstreams or []
        self.metadata = metadata or []

    def delete(
        self,
        client: DSpaceClient,
        item_uuid: str,
    ) -> Response:
        """Delete item and return the response.

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.HTTPError`: 404 Not Found if no item matching
                provided UUID
        """
        return client.delete(f"/items/{item_uuid}")

    def post(
        self,
        client: DSpaceClient,
        collection_handle: Optional[str] = None,
        collection_uuid: Optional[str] = None,
    ) -> Response:
        """Post item to a collection and return the response.

        Requires either the `collection_handle` or the `collection_uuid`, but not both.
        If both are passed, defaults to using the UUID.

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class
            collection_handle: The handle of an existing collection in DSpace to post
                the item to
            collection_uuid: The UUID of an existing collection in DSpace to post the
                item to

        Returns:
            :class:`requests.Response` object

        Raises:
            :class:`requests.HTTPError`: 404 Not Found if no collection matching
                provided handle/UUID
            MissingIdentifierError: if neither `collection_handle` nor `collection_uuid`
                parameter is provided
        """
        collection_id = select_identifier(client, collection_handle, collection_uuid)
        endpoint = f"/collections/{collection_id}/items"
        metadata = {"metadata": [m.to_dict() for m in self.metadata]}
        logger.debug(
            f"Posting new item to {client.base_url}{endpoint} with metadata "
            f"{metadata}"
        )
        return client.post(endpoint, json=metadata)


class MetadataEntry:
    """Class representing a `DSpace MetadataEntry object`_.

    .. _DSpace MetadataEntry object: https://wiki.lyrasis.org/display/DSDOC6x/\
    REST+API#RESTAPI-MetadataEntryObject>`

    Args:
        key: DSpace metadata field name in qualified Dublin Core format, e.g.
            'dc.description.abstract'
        value: DSpace metadata field value, e.g. 'The abstract for this item'
        language: Language of the DSpace metadata field, e.g. 'en_US'

    Attributes:
        key (str): Name of the metadata entry
        value (str): Value of the metadata entry
        language (str, optional): Language of the metadata entry
    """

    def __init__(self, key: str, value: str, language: Optional[str] = None):
        self.key = key
        self.value = value
        self.language = language

    def to_dict(self) -> dict:
        """Method to convert the MetadataEntry object to a dict.

        Returns:
            Dict representation of the metadata entry
        """
        return {key: value for key, value in self.__dict__.items() if value}

    @classmethod
    def from_dict(cls, entry: Dict[str, str]) -> MetadataEntry:
        """Class method to create a MetadataEntry object from a dict.

        Args:
            entry: A dict representing a DSpace metadata field name, value, and
                optionally language. Dict must be structured as follows::

                    {
                        "key": "dc.title",
                        "value": "Item Title",
                        "language": "en_US" [Optional]
                    }

        Returns:
            : class: `MetadataEntry` object

        Raises:
            : class: `KeyError`: if metadata entry dict does not contain both "key" and
                "value" items
        """
        return cls(
            key=entry["key"], value=entry["value"], language=entry.get("language", None)
        )
