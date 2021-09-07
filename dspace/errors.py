# dspace/errors.py
"""DSpace errors module.

This module includes custom Error classes that may be raised by DSpace Python client
library.
"""


class DSpacePythonError(Exception):
    """Base class for errors raise by the dspace-python-client library."""


class MissingFilePathError(DSpacePythonError):
    """Exception raised when required file_path attribute is not set on a bitstream.

    Args:
        expression: Input expression in which the error occurred

    Attributes:
        expression (str): Input expression in which the error occurred
        message (str): Explanation of the error
    """

    def __init__(self, expression: str):
        message = "Bitstream requires a file_path for this operation."
        super().__init__(message)
        self.expression = expression


class MissingIdentifierError(DSpacePythonError):
    """Exception raised when required identifier is not provided.

    Raised when neither a handle nor a uuid is provided to a request that requires one
    of the two.

    Args:
        expression: Input expression in which the error occurred

    Attributes:
        expression (str): Input expression in which the error occurred
        message (str): Explanation of the error
    """

    def __init__(self, expression: str):
        message = "Operation requires either a handle or an uuid."
        super().__init__(message)
        self.expression = expression
