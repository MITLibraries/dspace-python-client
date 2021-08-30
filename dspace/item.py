# dspace/item.py
"""dspace.item

This module includes classes representing DSpace Item and MetadataEntry objects, along
with functions for interacting with the DSpace REST API "/items" endpoint.
"""

from __future__ import annotations

import json
from typing import Dict, List, Optional

import structlog
from requests import Response

from dspace.client import DSpaceClient

logger = structlog.get_logger(__name__)


class Item:
    """Class representing a DSpace Item object and its associated API calls.

    Args:
        bitstreams: Bitstream objects to associate with the item
        metadata: :class:`MetadataEntry` objects to associate with the item

    Attributes:
        bitstreams (list): List of Bitstream objects belonging to the item
        metadata (list of :obj:`MetadataEntry`): List of
            :class:`MetadataEntry` objects representing the item's metadata

    """

    def __init__(
        self,
        bitstreams: Optional[List] = None,
        metadata: Optional[List[MetadataEntry]] = None,
    ):
        self.bitstreams = bitstreams or []
        self.metadata = metadata or []

    def post(self, client: DSpaceClient, collection_uuid: str) -> Response:
        """Post item to a collection and return the response

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class
            collection_id: The UUID (not the handle) of the DSpace collection to post
                the item to

        Raises:
            :class:`requests.HTTPError`: 404 Not Found if no collection matching provided
                UUID
        """

        endpoint = f"/collections/{collection_uuid}/items"
        metadata = {"metadata": [m.to_json() for m in self.metadata]}
        logger.debug(
            f"Posting new item to {client.base_url}{endpoint} with metadata "
            f"{metadata}"
        )
        return client.post(endpoint, json=metadata)


class MetadataEntry:
    """Class representing a `DSpace MetadataEntry object <https://wiki.lyrasis.org/
    display/DSDOC6x/REST+API#RESTAPI-MetadataEntryObject>`_.

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

    def to_json(self) -> str:
        """Method to convert the MetadataEntry object to a JSON string

        Returns:
            JSON string representation of the metadata entry
        """
        return json.dumps({key: value for key, value in self.__dict__.items() if value})

    @classmethod
    def from_dict(cls, entry: Dict[str, str]) -> MetadataEntry:
        """
        Class method to create a MetadataEntry object from a dict.

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
