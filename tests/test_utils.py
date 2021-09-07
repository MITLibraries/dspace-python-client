# tests/test_utils.py
import pytest

from dspace.errors import MissingIdentifierError
from dspace.utils import select_identifier


def test_select_identifier_with_handle(my_vcr, test_client, vcr_env):
    with my_vcr.use_cassette("vcr_cassettes/client/get_object_by_handle.yaml"):
        id = select_identifier(test_client, handle="1721.1/130884", uuid=None)
        assert id == "72dfcada-de27-4ce7-99cc-68266ebfd00c"


def test_select_identifier_with_uuid(test_client):
    id = select_identifier(test_client, handle=None, uuid="123456")
    assert id == "123456"


def test_select_identifier_without_id_raises_error(test_client):
    with pytest.raises(MissingIdentifierError):
        select_identifier(test_client, None, None)
