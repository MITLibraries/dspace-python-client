# dspace/item.py
"""DSpace item module.

This module includes classes representing DSpace Item and MetadataEntry objects, along
with functions for interacting with the DSpace REST API "/items" endpoint.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from dspace.bitstream import Bitstream
from dspace.client import DSpaceClient
from dspace.utils import select_identifier

logger = logging.getLogger(__name__)


class Item:
    """Class representing a DSpace Item object and its associated API calls.

    Args:
        bitstreams: :class:`Bitstream` objects to associate with the item
        metadata: :class:`MetadataEntry` objects to associate with the item

    Attributes:
        archived (Optional[str]): Item archived status in DSpace ("true" or "false")
        bitstreams (Optional[List[:obj:`Bitstream`]]): List of :class:`Bitstream`
            objects belonging to the item
        expand (List[str]): The expand options for the DSpace REST object
        handle (Optional[str]): The handle of the item in DSpace
        lastModified (Optional[str]): Timestamp the item was last modified in DSpace
        link (Optional[str]): The DSpace REST API path for the item
        metadata (Optional[List:obj:`MetadataEntry`]]): List of
            :class:`MetadataEntry` objects representing the item's metadata
        name (Optional[str]): The name of the item in DSpace
        parentCollection (Optional[str]): Parent collection of the item in DSpace
        parentCollectionList (Optiona[List[str]]): List of parent collections of the
            item in DSpace
        parentCommunityList (Optional[List[str]]): List of parent communities of the
            item in DSpace
        type (str): The DSpace object type
        uuid (Optional[str]): The internal UUID of the item in DSpace
        withdrawn (Optional[str]): Item withdrawn status in DSpace ("true" or "false")
    """

    def __init__(
        self,
        bitstreams: Optional[List[Bitstream]] = None,
        metadata: Optional[List[MetadataEntry]] = None,
    ):
        self.bitstreams = bitstreams or []
        self.metadata = metadata or []

        self.archived = None
        self.expand = [
            "metadata",
            "parentCollection",
            "parentCollectionList",
            "parentCommunityList",
            "bitstreams",
            "all",
        ]
        self.handle = None
        self.lastModified = None
        self.link = None
        self.name = None
        self.parentCollection = None
        self.parentCollectionList = None
        self.parentCommunityList = None
        self.type = "item"
        self.uuid = None
        self.withdrawn = None

    def delete(self, client: DSpaceClient) -> None:
        """Delete item from DSpace and unset relevant item attributes.

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class

        Raises:
            :class:`requests.HTTPError`: 404 Not Found if no item matching
                provided UUID
        """
        logger.debug("Deleting item with uuid %s from %s", self.uuid, client.base_url)
        response = client.delete(f"/items/{self.uuid}")
        logger.debug("Delete response: %s", response)
        self.archived = None
        self.handle = None
        self.lastModified = None
        self.link = None
        self.name = None
        self.parentCollection = None
        self.parentCollectionList = None
        self.parentCommunityList = None
        self.uuid = None
        self.withdrawn = None

    def post(
        self,
        client: DSpaceClient,
        collection_handle: Optional[str] = None,
        collection_uuid: Optional[str] = None,
    ) -> None:
        """Post item to a collection and set item attributes to response object values.

        Requires either the `collection_handle` or the `collection_uuid`, but not both.
        If both are passed, defaults to using the UUID.

        Args:
            client: An authenticated instance of the :class:`DSpaceClient` class
            collection_handle: The handle of an existing collection in DSpace to post
                the item to
            collection_uuid: The UUID of an existing collection in DSpace to post the
                item to

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
            "Posting new item to %s with metadata %s",
            client.base_url + endpoint,
            metadata,
        )
        response = client.post(endpoint, json=metadata).json()
        logger.debug("Post response: %s", response)
        self.archived = response["archived"]
        self.handle = response["handle"]
        self.lastModified = response["lastModified"]
        self.link = response["link"]
        self.name = response["name"]
        self.parentCollection = response["parentCollection"]
        self.parentCollectionList = response["parentCollectionList"]
        self.parentCommunityList = response["parentCommunityList"]
        self.uuid = response["uuid"]
        self.withdrawn = response["withdrawn"]


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
        language (Optional[str]): Language of the metadata entry
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
