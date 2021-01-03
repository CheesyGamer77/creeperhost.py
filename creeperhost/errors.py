class CreeperhostException(Exception):
    """
    Base exception for all errors returned by the CreeperHost API.

    All exceptions thrown by the library derive from this base class
    """

    pass


class HTTPException(CreeperhostException):
    """
    Base exception for all HTTP exceptions returned by the API.
    """

    pass


class Forbidden(HTTPException):
    """
    Thrown when an HTTP 403 status is returned
    """

    pass


class NotFound(HTTPException):
    """
    Thrown when an HTTP 404 status is returned
    """

    pass


class ServerError(HTTPException):
    """
    Thrown when an HTTP 500+ status is returned
    """

    pass