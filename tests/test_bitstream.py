# tests/test_bitstream.py
import pytest
import requests

from dspace.bitstream import Bitstream
from dspace.errors import MissingFilePathError, MissingIdentifierError


def test_bitstream_delete(my_vcr, test_client):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/bitstream/delete_bitstream.yaml",
    ):
        bitstream = Bitstream()
        bitstream.uuid = "9df9382c-d332-4ddc-a77a-e8e6e3f1bcff"
        bitstream.delete(test_client)
        assert bitstream.uuid is None


def test_bitstream_delete_nonexistent_bitstream_raises_error(my_vcr, test_client):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/bitstream/delete_nonexistent_bitstream.yaml",
    ):
        with pytest.raises(requests.HTTPError):
            bitstream = Bitstream()
            bitstream.uuid = "5-7-4-b-0"
            bitstream.delete(test_client)


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
        bitstream.post(test_client, item_handle="1721.1/131167")
        assert bitstream.bundleName == "ORIGINAL"
        assert bitstream.checkSum == {
            "value": "8bfa8e0684108f419933a5995264d150",
            "checkSumAlgorithm": "MD5",
        }
        assert bitstream.format == "Text"
        assert bitstream.link == "/rest/bitstreams/2546ae0a-152a-4e0d-ad2d-28f62f301529"
        assert bitstream.mimeType == "text/plain"
        assert bitstream.parentObject is None
        assert bitstream.policies is None
        assert bitstream.retrieveLink == (
            "/rest/bitstreams/2546ae0a-152a-4e0d-ad2d-28f62f301529/retrieve"
        )
        assert bitstream.sequenceId == -1
        assert bitstream.sizeBytes == 12
        assert bitstream.uuid == "2546ae0a-152a-4e0d-ad2d-28f62f301529"


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
        bitstream.post(test_client, item_handle="1721.1/131167")
        assert bitstream.bundleName == "ORIGINAL"
        assert bitstream.checkSum == {
            "value": "a4e0f4930dfaff904fa3c6c85b0b8ecc",
            "checkSumAlgorithm": "MD5",
        }
        assert bitstream.format == "Adobe PDF"
        assert bitstream.link == "/rest/bitstreams/d1a3ca4f-1e79-442b-a204-49462ce14b07"
        assert bitstream.mimeType == "application/pdf"
        assert bitstream.parentObject is None
        assert bitstream.policies is None
        assert bitstream.retrieveLink == (
            "/rest/bitstreams/d1a3ca4f-1e79-442b-a204-49462ce14b07/retrieve"
        )
        assert bitstream.sequenceId == -1
        assert bitstream.sizeBytes == 35721
        assert bitstream.uuid == "d1a3ca4f-1e79-442b-a204-49462ce14b07"


def test_bitstream_post_success_with_uuid(my_vcr, test_client, test_file_path_01):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/bitstream/post_bitstream_with_uuid.yaml",
        filter_post_data_parameters=None,
    ):
        bitstream = Bitstream(file_path=test_file_path_01)
        bitstream.post(test_client, item_uuid="b3bc3232-a1ff-49ec-b816-aa8ebde60258")
        assert bitstream.bundleName == "ORIGINAL"
        assert bitstream.checkSum == {
            "value": "a4e0f4930dfaff904fa3c6c85b0b8ecc",
            "checkSumAlgorithm": "MD5",
        }
        assert bitstream.format == "Unknown"
        assert bitstream.link == "/rest/bitstreams/106f5e94-b5ac-436c-b3f8-4e01210a5b63"
        assert bitstream.mimeType == "application/octet-stream"
        assert bitstream.parentObject is None
        assert bitstream.policies is None
        assert bitstream.retrieveLink == (
            "/rest/bitstreams/106f5e94-b5ac-436c-b3f8-4e01210a5b63/retrieve"
        )
        assert bitstream.sequenceId == -1
        assert bitstream.sizeBytes == 35721
        assert bitstream.uuid == "106f5e94-b5ac-436c-b3f8-4e01210a5b63"


def test_bitstream_post_to_nonexistent_item_raises_error(
    my_vcr, test_client, test_file_path_01
):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/bitstream/post_to_nonexistent_item.yaml",
        filter_post_data_parameters=None,
    ):
        with pytest.raises(requests.HTTPError):
            bitstream = Bitstream(file_path=test_file_path_01)
            bitstream.post(test_client, item_uuid="123456")


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
