# tests/test_bitstream.py
import pytest
import requests

from dspace.bitstream import Bitstream
from dspace.errors import MissingFilePathError, MissingIdentifierError


def test_bitstream_post_success_remote_file(my_vcr, test_client, mocked_s3):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/bitstream/post_bitstream_success_remote_file.yaml",
        filter_post_data_parameters=None,
    ):
        bitstream = Bitstream(
            name="test-file-03.txt",
            description="A test TXT file",
            file_path="s3://test-bucket/path/file/test-file-03.txt",
        )
        response = bitstream.post(test_client, item_handle="1721.1/131167")
        assert response.status_code == 200
        assert response.json()["description"] == "A test TXT file"
        assert response.json()["name"] == "test-file-03.txt"
        assert response.json()["type"] == "bitstream"


def test_bitstream_post_success_with_handle(my_vcr, test_client, test_file_path_01):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/bitstream/post_bitstream_with_handle.yaml",
        filter_post_data_parameters=None,
    ):
        bitstream = Bitstream(
            name="test-file-01.pdf",
            description="A test PDF file",
            file_path=test_file_path_01,
        )
        response = bitstream.post(test_client, item_handle="1721.1/131167")
        assert response.status_code == 200
        assert response.json()["description"] == "A test PDF file"
        assert response.json()["name"] == "test-file-01.pdf"
        assert response.json()["type"] == "bitstream"


def test_bitstream_post_success_with_uuid(my_vcr, test_client, test_file_path_01):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/bitstream/post_bitstream_with_uuid.yaml",
        filter_post_data_parameters=None,
    ):
        bitstream = Bitstream(file_path=test_file_path_01)
        response = bitstream.post(
            test_client, item_uuid="b3bc3232-a1ff-49ec-b816-aa8ebde60258"
        )
        assert response.status_code == 200
        assert response.json()["description"] is None
        assert response.json()["name"] is None
        assert response.json()["type"] == "bitstream"


def test_bitstream_post_to_nonexistent_item_raises_error(
    my_vcr, test_client, test_file_path_01
):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/bitstream/post_to_nonexistent_item.yaml",
        filter_post_data_parameters=None,
    ):
        with pytest.raises(requests.HTTPError):
            bitstream = Bitstream(file_path=test_file_path_01)
            response = bitstream.post(test_client, item_uuid="123456")
            assert "404" in response.text


def test_bitstream_post_without_file_path_raises_error(test_client, test_file_path_01):
    with pytest.raises(MissingFilePathError):
        bitstream = Bitstream()
        bitstream.post(test_client, item_handle="1721.1/131167")


def test_bitstream_post_without_handle_or_uuid_raises_error(
    test_client, test_file_path_01
):
    with pytest.raises(MissingIdentifierError):
        bitstream = Bitstream(file_path=test_file_path_01)
        bitstream.post(test_client)
