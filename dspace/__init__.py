# dspace/__init__.py
"""DSpace Python Client package."""
import logging

from dspace.bitstream import Bitstream
from dspace.client import DSpaceClient
from dspace.item import Item, MetadataEntry

logging.getLogger(__name__).addHandler(logging.NullHandler())
