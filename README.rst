====================
dspace-python-client
====================

A Python client library for working with the DSpace API. This was written against the `DSpace version 6.x API <https://wiki.lyrasis.org/display/DSDOC6x/REST+API>`_ and will not work with later versions of DSpace.

-----
Usage
-----

To install this library with `pip`::

  pip install "git+https://github.com/mitlibraries/dspace-python-client.git@<release-version-number>#egg=dspace-python-client"

To install this library with `pipenv`::

  pipenv install "git+https://github.com/mitlibraries/dspace-python-client.git@<release-version-number>#egg=dspace-python-client"

To authenticate the DSpace client::

  from dspace.bitstream import Bitstream
  from dspace.client import DSpaceClient
  from dspace.item import Item, MetadataEntry
  
  client = DSpaceClient(<DSpace API URL>)
  client.login(<your email>, <your password>)

To post an item and associated bitstream with an authenticated client::
  
  title = MetadataEntry(key="dc.title", value="Test Item")
  item = Item(metadata=[title])
  item.post(client, collection_handle=<valid DSpace handle e.g. "1234.5/6789">)

  bitstream = Bitstream(name="test.txt", file_path="test.txt")
  bitstream.post(client, item_uuid=item.uuid)
  

------------
Development
------------

^^^^^^^^^^^^
Dependencies
^^^^^^^^^^^^
~~~~~~
Python
~~~~~~

Version 3.9

~~~~~~
Poetry
~~~~~~
This project uses Poetry for dependency management and packaging.

You only need to install Poetry once, so if you've already installed it for another project you can skip this step. Poetry will automatically pick up the current Python version and use it to create virtualenvs accordingly.

To install poetry:

* Mac/unix::

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

* Windows::

    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -

Run ``poetry --version`` to confirm installation.

See `Poetry installation docs <https://python-poetry.org/docs/#installation>`_ for configuration options and more information.

^^^^^^^^^^^^
Installation
^^^^^^^^^^^^

Install dspace-python-client for local development by running::

  git clone https://github.com/MITLibraries/dspace-python-client.git
  cd dspace-python-client
  make install

^^^^^
Tests
^^^^^
Tests can be run with ``make test``.

This project uses `vcrpy <https://vcrpy.readthedocs.io/en/latest/>`_ to create test cassettes of real data for API calls. If you need to recreate the test cassettes or add new ones:

1. Create a .env file with the following variables::

    DSPACE_PYTHON_CLIENT_ENV=vcr_create_cassettes
    TEST_DSPACE_API_URL=<your test DSpace instance API url>
    TEST_DSPACE_EMAIL=<your test DSpace instance email>
    TEST_DSPACE_PASSWORD=<your test DSpace instance password>

2. Delete any test cassettes you want to replace. VCR is set to run once, meaning it will not overwrite existing cassettes.

3. If the tests you want to create cassettes for use the ``test_client`` fixture, you will need to update it. In ``tests/conftest.py``, comment out the ``with my_vcr.use_cassette(...`` line of the ``test_client`` fixture and adjust the indenting so the whole fixture function looks like this::

    @pytest.fixture
    def test_client(my_vcr, vcr_env):
        # with my_vcr.use_cassette("tests/vcr_cassettes/client/login.yaml"):
        client = DSpaceClient(vcr_env["url"])
        client.login(vcr_env["email"], vcr_env["password"])
        return client

4. Run ``make test`` to run the tests. This will run all tests with API calls against *your real* DSpace test instance and record the requests/responses as cassettes.

5. Review new cassettes to make sure no sensitive data has been recorded. If it has, add to the vcr functions in ``conftest.py`` to scrub the sensitive data and rerun ``make test`` to confirm.

6. *VERY IMPORTANT*: comment out the ``DSPACE_PYTHON_CLIENT_ENV`` variable in your .env file. And reset the `test_client` fixture to its previous state. This ensures that future local test runs use the cassettes instead of making calls to the real DSpace API.

7. Run ``make test`` again to confirm that your cassettes are working properly.
