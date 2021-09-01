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


def test_client_get_method(my_vcr, vcr_env):
    with my_vcr.use_cassette("tests/vcr_cassettes/client/status.yaml"):
        client = DSpaceClient(vcr_env["url"])
        response = client.get("/status")
        assert isinstance(response, requests.Response)


def test_client_get_object_by_handle(my_vcr, test_client, vcr_env):
    with my_vcr.use_cassette("tests/vcr_cassettes/client/get_object_by_handle.yaml"):
        collection = test_client.get_object_by_handle("1721.1/130884").json()
        assert collection["name"] == "Graduate Theses"
        assert collection["type"] == "collection"
        assert collection["uuid"] == "72dfcada-de27-4ce7-99cc-68266ebfd00c"


def test_client_get_object_by_handle_raises_error_if_doesnt_exist(
    my_vcr, test_client, vcr_env
):
    with my_vcr.use_cassette(
        "tests/vcr_cassettes/client/get_object_by_handle_doesnt_exist.yaml"
    ):
        with pytest.raises(requests.HTTPError):
            test_client.get_object_by_handle("1721.1/000000")


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


def test_client_post_method(my_vcr, vcr_env):
    with my_vcr.use_cassette("tests/vcr_cassettes/client/login.yaml"):
        client = DSpaceClient(vcr_env["url"])
        response = client.post(
            "/login", data={"email": vcr_env["email"], "password": vcr_env["password"]}
        )
        assert isinstance(response, requests.Response)


def test_client_status(my_vcr, test_client, vcr_env):
    with my_vcr.use_cassette("tests/vcr_cassettes/client/status.yaml"):
        status = test_client.status().json()
        assert status["okay"] is True
        assert status["authenticated"] is True
