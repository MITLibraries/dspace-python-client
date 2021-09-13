# dspace.utils.py
"""DSpace utils module.

Utility functions for the DSpace Python client library.
"""

import logging
from typing import Optional

from dspace.client import DSpaceClient
from dspace.errors import MissingIdentifierError

logger = logging.getLogger(__name__)


def select_identifier(
    client: DSpaceClient, handle: Optional[str], uuid: Optional[str]
) -> str:
    """Return the uuid of a DSpace object given a handle, a uuid, or both.

    Args:
        client: Authenticated instance of :class:`DSpaceClient` class
        handle: Handle of a DSpace object
        uuid: UUID of a DSpace object

    Returns:
        UUID of DSpace object

    Raises:
        :class:`requests.HTTPError`: 404 Not Found if no DSpace object exists matching
            provided handle
        :class:`MissingIdentifierError`: if neither a handle nor a UUID is provided
    """
    if uuid:
        return uuid
    elif handle:
        retrieved_uuid = client.get_object_by_handle(handle).json()["uuid"]
        return retrieved_uuid
    else:
        raise MissingIdentifierError(f"bitstream.post({client}, {uuid})")
