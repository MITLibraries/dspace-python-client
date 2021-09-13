# tests/test_item.py
import pytest
import requests

from dspace.errors import MissingIdentifierError
from dspace.item import Item, MetadataEntry


def test_item_delete(my_vcr, test_client):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/item/delete_item.yaml",
    ):
        item = Item()
        item.uuid = "1becd094-9fe8-4625-ab55-86520441a1ca"
        item.delete(test_client)
        assert item.uuid is None


def test_item_delete_nonexistent_item_raises_error(my_vcr, test_client):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/item/delete_nonexistent_item.yaml",
    ):
        with pytest.raises(requests.HTTPError):
            item = Item()
            item.uuid = "5-7-4-b-0"
            item.delete(test_client)


def test_item_instantiates_with_expected_values():
    title = MetadataEntry(key="dc.title", value="Test Item")
    item = Item(metadata=[title])
    assert item.bitstreams == []
    assert item.metadata == [title]


def test_item_post_success_with_handle(my_vcr, test_client):
    with my_vcr.use_cassette("tests/vcr_cassettes/item/post_item_with_handle.yaml"):
        item = Item(
            metadata=[
                MetadataEntry(key="dc.title", value="Test Item"),
                MetadataEntry(key="dc.contributor.author", value="Jane Q. Author"),
            ]
        )
        item.post(test_client, collection_handle="1721.1/130884")
        assert item.archived == "true"
        assert item.handle == "1721.1/131194"
        assert item.lastModified == "Thu Sep 02 14:57:52 UTC 2021"
        assert item.parentCollection is None
        assert item.parentCollectionList is None
        assert item.parentCommunityList is None
        assert item.link == "/rest/items/229451b3-e943-46e8-a27e-f45d5c8aa0ec"
        assert item.name == "Test Item"
        assert item.uuid == "229451b3-e943-46e8-a27e-f45d5c8aa0ec"
        assert item.withdrawn == "false"


def test_item_post_success_with_uuid(my_vcr, test_client):
    with my_vcr.use_cassette("tests/vcr_cassettes/item/post_item_with_uuid.yaml"):
        item = Item(
            metadata=[
                MetadataEntry(key="dc.title", value="Test Item"),
                MetadataEntry(key="dc.contributor.author", value="Jane Q. Author"),
            ]
        )
        item.post(test_client, collection_uuid="72dfcada-de27-4ce7-99cc-68266ebfd00c")
        assert item.archived == "true"
        assert item.handle == "1721.1/131195"
        assert item.lastModified == "Thu Sep 02 14:57:55 UTC 2021"
        assert item.link == "/rest/items/7e48085d-1cdf-4b37-8d56-ae44683b5d9a"
        assert item.name == "Test Item"
        assert item.parentCollection is None
        assert item.parentCollectionList is None
        assert item.parentCommunityList is None
        assert item.uuid == "7e48085d-1cdf-4b37-8d56-ae44683b5d9a"
        assert item.withdrawn == "false"


def test_item_post_to_nonexistent_collection_raises_error(my_vcr, test_client):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/item/post_to_nonexistent_collection.yaml"
    ):
        with pytest.raises(requests.HTTPError):
            item = Item()
            item.post(test_client, collection_uuid="123456")


def test_item_post_without_handle_or_uuid_raises_error(test_client):
    with pytest.raises(MissingIdentifierError):
        item = Item()
        item.post(test_client)


def test_metadata_entry_instantiates_with_expected_values():
    metadata_entry = MetadataEntry("dc.fieldname", "field value")
    assert metadata_entry.key == "dc.fieldname"
    assert metadata_entry.value == "field value"
    assert metadata_entry.language is None


def test_metadata_entry_to_dict():
    metadata_entry = MetadataEntry("dc.fieldname", "field value")
    metadata_entry_dict = metadata_entry.to_dict()
    assert metadata_entry_dict == {"key": "dc.fieldname", "value": "field value"}


def test_metadata_entry_from_dict():
    test_entry = {"key": "dc.fieldname", "value": "field value"}
    metadata_entry = MetadataEntry.from_dict(test_entry)
    assert isinstance(metadata_entry, MetadataEntry)
    assert metadata_entry.key == "dc.fieldname"
    assert metadata_entry.value == "field value"
    assert metadata_entry.language is None


def test_metadata_entry_from_dict_raises_error_if_missing_fields():
    with pytest.raises(KeyError):
        test_entry = {"value": "field value"}
        MetadataEntry.from_dict(test_entry)
        MetadataEntry.from_dict(test_entry)
