import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from app.clients.exceptions import (
    NHTSABadRequestError,
    NHTSAHTTPError,
    NHTSANotFoundError,
    NHTSATimeoutError,
    NHTSAUnavailableError,
)

logger = logging.getLogger(__name__)


def nhtsa_bad_request_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, NHTSABadRequestError)

    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


def nhtsa_timeout_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, NHTSATimeoutError)

    logger.error(
        "NHTSA timeout while handling %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )
    return JSONResponse(
        status_code=504,
        content={"detail": str(exc)},
    )


def nhtsa_unavailable_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, NHTSAUnavailableError)

    logger.error(
        "NHTSA unavailable while handling %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )


def nhtsa_not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, NHTSANotFoundError)

    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


def nhtsa_http_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, NHTSAHTTPError)

    logger.error(
        "NHTSA upstream error while handling %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )

    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)},
    )


def database_unavailable_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, OperationalError)

    logger.error(
        "Database unavailable while handling %s %s: %s",
        request.method,
        request.url.path,
        exc,
    )

    return JSONResponse(
        status_code=503,
        content={"detail": "Database unavailable"},
    )
