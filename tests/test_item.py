# tests/test_item.py
import pytest
import requests

from dspace.item import Item, MetadataEntry


def test_item_instantiates_with_expected_values():
    title = MetadataEntry(key="dc.title", value="Test Item")
    item = Item(metadata=[title])
    assert item.bitstreams == []
    assert item.metadata == [title]


def test_item_post(my_vcr, test_client):
    with my_vcr.use_cassette("tests/vcr_cassettes/item/post.yaml"):
        item = Item(metadata=[MetadataEntry(key="dc.title", value="Test Item")])
        response = item.post(test_client, "72dfcada-de27-4ce7-99cc-68266ebfd00c").json()
        assert response["handle"] == "1721.1/131167"
        assert response["lastModified"] == "Fri Aug 27 13:42:16 UTC 2021"
        assert response["link"] == "/rest/items/b3bc3232-a1ff-49ec-b816-aa8ebde60258"
        assert response["name"] == "Test Item"
        assert response["type"] == "item"
        assert response["uuid"] == "b3bc3232-a1ff-49ec-b816-aa8ebde60258"


def test_item_post_to_nonexistent_collection_raises_error(my_vcr, test_client):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/item/post_to_nonexistent_collection.yaml"
    ):
        with pytest.raises(requests.HTTPError):
            item = Item()
            response = item.post(test_client, "123456")
            assert "404" in response.text


def test_metadata_entry_instantiates_with_expected_values():
    metadata_entry = MetadataEntry("dc.fieldname", "field value")
    assert metadata_entry.key == "dc.fieldname"
    assert metadata_entry.value == "field value"
    assert metadata_entry.language is None


def test_metadata_entry_to_json():
    metadata_entry = MetadataEntry("dc.fieldname", "field value")
    metadata_entry_json = metadata_entry.to_json()
    assert metadata_entry_json == '{"key": "dc.fieldname", "value": "field value"}'


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
