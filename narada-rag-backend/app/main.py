import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.CHATREQUEST.index import ChatRequest
from app.config import Settings, get_settings
from app.models import ErrorDetail, ErrorResponse, HealthResponse, ValidationIssue

logger = logging.getLogger(__name__)


def _error_response(
    request: Request,
    *,
    status_code: int,
    code: str,
    message: str,
    details: list[ValidationIssue] | None = None,
) -> JSONResponse:
    response = ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            request_id=request.state.request_id,
            details=details,
        )
    )
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(mode="json", exclude_none=True),
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    application = FastAPI(title=app_settings.app_name)

    @application.middleware("http")
    async def add_request_id(request: Request, call_next):
        request.state.request_id = str(uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        return response

    @application.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request,
        exception: RequestValidationError,
    ) -> JSONResponse:
        issues = []
        for error in exception.errors():
            location = [part for part in error.get("loc", ()) if part != "body"]
            issues.append(
                ValidationIssue(
                    field=".".join(str(part) for part in location) or "body",
                    message=error.get("msg", "Invalid value"),
                    code=error.get("type", "invalid"),
                )
            )
        return _error_response(
            request,
            status_code=422,
            code="validation_error",
            message="Request validation failed.",
            details=issues,
        )

    @application.exception_handler(StarletteHTTPException)
    async def handle_http_error(
        request: Request,
        exception: StarletteHTTPException,
    ) -> JSONResponse:
        message = (
            exception.detail
            if isinstance(exception.detail, str)
            else "Request failed."
        )
        return _error_response(
            request,
            status_code=exception.status_code,
            code="http_error",
            message=message,
        )

    @application.exception_handler(Exception)
    async def handle_unexpected_error(
        request: Request,
        exception: Exception,
    ) -> JSONResponse:
        logger.error(
            "Unhandled API error",
            extra={
                "request_id": request.state.request_id,
                "error_type": type(exception).__name__,
            },
        )
        return _error_response(
            request,
            status_code=500,
            code="internal_error",
            message="An unexpected error occurred.",
        )

    @application.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @application.get("/ready", response_model=HealthResponse)
    async def readiness() -> HealthResponse:
        return HealthResponse(status="ready")

    @application.post(
        "/api/chat",
        status_code=501,
        responses={501: {"model": ErrorResponse}},
    )
    async def chat(request: Request, _: ChatRequest) -> JSONResponse:
        return _error_response(
            request,
            status_code=501,
            code="chat_not_implemented",
            message="Chat generation is not implemented.",
        )

    return application


app = create_app()
