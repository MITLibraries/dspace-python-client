# tests/test_client.py

import pytest
import requests

from dspace.client import DSpaceClient


def test_client_instantiates_with_expected_values():
    client = DSpaceClient("https://dspace-example.com/rest")
    assert client.headers["accept"] == "application/json"
    assert client.base_url == "https://dspace-example.com/rest"


def test_client_repr():
    client = DSpaceClient("https://dspace-example.com/rest")
    assert str(client) == (
        "DSpaceClient(base_url='https://dspace-example.com/rest', "
        "accept_header='application/json')"
    )


def test_client_login(my_vcr, vcr_env):
    with my_vcr.use_cassette("tests/vcr_cassettes/client/login.yaml"):
        client = DSpaceClient(vcr_env["url"])
        assert "JSESSIONID" not in client.cookies
        client.login(vcr_env["email"], vcr_env["password"])
        assert "JSESSIONID" in client.cookies


def test_client_login_raises_auth_error(my_vcr, vcr_env):
    with my_vcr.use_cassette("tests/vcr_cassettes/client/login_error.yaml"):
        client = DSpaceClient(vcr_env["url"])
        with pytest.raises(requests.HTTPError):
            client.login("fake_user@example.com", "fake_password")


def test_client_status(my_vcr, vcr_env):
    with my_vcr.use_cassette("tests/vcr_cassettes/client/status.yaml"):
        client = DSpaceClient(vcr_env["url"])
        status = client.status()
        assert status["authenticated"] is False
        client.login(vcr_env["email"], vcr_env["password"])
        status = client.status()
        assert status["authenticated"] is True
