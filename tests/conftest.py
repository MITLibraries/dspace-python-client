# test/conftest.py
import json
import os
import urllib

import pytest
import vcr
from dotenv import load_dotenv

from dspace.client import DSpaceClient

load_dotenv()


@pytest.fixture
def my_vcr():
    my_vcr = vcr.VCR(
        before_record_request=vcr_scrub_request,
        before_record_response=vcr_scrub_response,
        decode_compressed_response=True,
        filter_post_data_parameters=[
            ("email", "user@example.com"),
            ("password", "password"),
        ],
        filter_headers=[("Cookie", "JSESSIONID=sessioncookie")],
    )
    return my_vcr


@pytest.fixture
def test_client(my_vcr, vcr_env):
    with my_vcr.use_cassette("tests/vcr_cassettes/client/login.yaml"):
        client = DSpaceClient(vcr_env["url"])
        client.login(vcr_env["email"], vcr_env["password"])
        return client


@pytest.fixture
def vcr_env():
    if os.getenv("DSPACE_PYTHON_CLIENT_ENV") == "vcr_create_cassettes":
        env = {
            "url": os.environ["TEST_DSPACE_API_URL"],
            "email": os.environ["TEST_DSPACE_EMAIL"],
            "password": os.environ["TEST_DSPACE_PASSWORD"],
        }
    else:
        env = {
            "url": "https://dspace-example.com/rest",
            "email": "user@example.com",
            "password": "password",
        }
    return env


def vcr_scrub_request(request):
    """Replaces the request URI with fake data"""
    split_uri = urllib.parse.urlsplit(request.uri)
    new_uri = urllib.parse.urljoin("https://dspace-example.com", split_uri.path)
    request.uri = new_uri
    return request


def vcr_scrub_response(response):
    """Replaces the response session cookie and any user data in the response body with
    fake data. Also replaces response body content that isn't needed for testing."""
    if "Set-Cookie" in response["headers"]:
        response["headers"]["Set-Cookie"] = [
            "JSESSIONID=sessioncookie; Path=/rest; Secure; HttpOnly"
        ]
    try:
        response_json = json.loads(response["body"]["string"])
    except json.decoder.JSONDecodeError:
        pass
    else:
        response_json.pop("introductoryText", None)
        try:
            email = response_json["email"]
            if email is not None:
                response_json["email"] = "user@example.com"
                response_json["fullname"] = "Test User"
        except (KeyError, TypeError):
            pass
        if response_json != json.loads(response["body"]["string"]):
            response["body"]["string"] = json.dumps(response_json)
    return response
