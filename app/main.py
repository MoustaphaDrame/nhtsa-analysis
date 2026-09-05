from fastapi import FastAPI

from app.api.exceptions_handlers import (
    nhtsa_bad_request_handler,
    nhtsa_http_error_handler,
    nhtsa_timeout_handler,
    nhtsa_unavailable_handler,
    nhtsa_not_found_handler,
)

from app.clients.exceptions import (
    NHTSABadRequestError,
    NHTSATimeoutError,
    NHTSAUnavailableError,
    NHTSANotFoundError,
    NHTSAHTTPError
)

from app.api.routes.vehicles import router as vehicles_router


app = FastAPI(
    title="NHTSA Vehicle Complaints API"
)

app.add_exception_handler(
    NHTSABadRequestError,
    nhtsa_bad_request_handler,
)

app.add_exception_handler(
    NHTSATimeoutError,
    nhtsa_timeout_handler,
)

app.add_exception_handler(
    NHTSAUnavailableError,
    nhtsa_unavailable_handler,
)

app.add_exception_handler(
    NHTSANotFoundError,
    nhtsa_not_found_handler,
)

app.add_exception_handler(
    NHTSAHTTPError,
    nhtsa_http_error_handler,
)

app.include_router(vehicles_router)