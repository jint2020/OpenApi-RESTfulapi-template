from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.problem import InvalidParam, ProblemDetails

PROBLEM_JSON = "application/problem+json"


def build_problem(
    *,
    status: int,
    title: str,
    detail: str,
    instance: str,
    type_: str = "about:blank",
    invalid_params: list[InvalidParam] | None = None,
) -> ProblemDetails:
    return ProblemDetails(
        type=type_,
        title=title,
        status=status,
        detail=detail,
        instance=instance,
        invalid_params=invalid_params,
    )


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        problem = build_problem(
            status=exc.status_code,
            title="HTTP Error",
            detail=str(exc.detail),
            instance=str(request.url.path),
        )
        return JSONResponse(problem.model_dump(exclude_none=True), status_code=exc.status_code, media_type=PROBLEM_JSON)

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        invalid_params: list[InvalidParam] = []
        for err in exc.errors():
            location = ".".join(str(item) for item in err.get("loc", []))
            invalid_params.append(InvalidParam(name=location, reason=err.get("msg", "invalid value")))

        problem = build_problem(
            status=422,
            title="Validation Error",
            detail="Request payload or parameters failed validation.",
            instance=str(request.url.path),
            type_="https://example.com/problems/validation-error",
            invalid_params=invalid_params,
        )
        return JSONResponse(problem.model_dump(exclude_none=True), status_code=422, media_type=PROBLEM_JSON)

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        problem = build_problem(
            status=500,
            title="Internal Server Error",
            detail="An unexpected error occurred.",
            instance=str(request.url.path),
            type_="https://example.com/problems/internal-error",
        )
        return JSONResponse(problem.model_dump(exclude_none=True), status_code=500, media_type=PROBLEM_JSON)
