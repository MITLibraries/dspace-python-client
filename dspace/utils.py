# dspace.utils.py
"""dspace.utils

Utility functions for the DSpace Python client library.
"""

from typing import Optional

from dspace.client import DSpaceClient
from dspace.errors import MissingIdentifierError


def select_identifier(
    client: DSpaceClient, handle: Optional[str], uuid: Optional[str]
) -> str:
    """Return the uuid of an item given a handle, a uuid, or both.

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
        uuid = client.get_object_by_handle(handle).json()["uuid"]
        return uuid
    else:
        raise MissingIdentifierError(f"bitstream.post({client}, {uuid})")
