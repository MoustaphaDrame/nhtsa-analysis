from fastapi import Request
from fastapi.responses import JSONResponse

from app.clients.exceptions import (
    NHTSABadRequestError,
    NHTSAHTTPError,
    NHTSATimeoutError,
    NHTSAUnavailableError,
    NHTSANotFoundError,
)


def nhtsa_bad_request_handler(
    request: Request,
    exc: NHTSABadRequestError,
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


def nhtsa_timeout_handler(
    request: Request,
    exc: NHTSATimeoutError,
) -> JSONResponse:
    return JSONResponse(
        status_code=504,
        content={"detail": str(exc)},
    )


def nhtsa_unavailable_handler(
    request: Request,
    exc: NHTSAUnavailableError,
) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={"detail": str(exc)},
    )

def nhtsa_not_found_handler(
    request: Request,
    exc: NHTSANotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

def nhtsa_http_error_handler(
    request: Request,
    exc: NHTSAHTTPError,
) -> JSONResponse:
    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)},
    )