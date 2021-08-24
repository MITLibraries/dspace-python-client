====================
dspace-python-client
====================

A Python client library for working with the DSpace API. This was written against the `DSpace version 6.x API <https://wiki.lyrasis.org/display/DSDOC6x/REST+API>`_ and will not work with later versions of DSpace.

-----
Usage
-----

This project has not been released for active use yet. Check back soon!

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

2. Run ``make test`` to run the tests. This will run all tests with API calls against *your real* DSpace test instance and record the requests/responses as cassettes.

3. Review new cassettes to make sure no sensitive data has been recorded. If it has, add to the vcr functions in ``conftest.py`` to scrub the sensitive data and rerun ``make test`` to confirm.

4. *VERY IMPORTANT*: comment out the ``DSPACE_PYTHON_CLIENT_ENV`` variable in your .env file. This ensures that future local test runs use the cassettes instead of making calls to the real DSpace API.

5. Run ``make test`` again to confirm that your cassettes are working properly.
