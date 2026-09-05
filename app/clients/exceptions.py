class NHTSAClientError(Exception):
    """Base exception for NHTSA client errors."""


class NHTSATimeoutError(NHTSAClientError):
    """Raised when the NHTSA API does not respond in time."""


class NHTSAUnavailableError(NHTSAClientError):
    """Raised when the NHTSA API cannot be reached."""


class NHTSABadRequestError(NHTSAClientError):
    """Raised when the NHTSA API rejects the request."""

class NHTSANotFoundError(NHTSAClientError):
    """Raised when the requested NHTSA resource is not found."""

class NHTSAHTTPError(NHTSAClientError):
    """Raised for an unhandled HTTP error returned by the NHTSA API."""