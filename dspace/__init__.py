# dspace/__init__.py
"""DSpace Python Client package."""
import logging

from dspace.bitstream import Bitstream  # noqa
from dspace.client import DSpaceClient  # noqa
from dspace.item import Item, MetadataEntry  # noqa

logging.getLogger(__name__).addHandler(logging.NullHandler())
