from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api import api_router
from utils.helpers import AppError, normalize_validation_errors


def create_app() -> FastAPI:
    app = FastAPI(title="Echo", version="1.0.0")

    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=exc.to_dict())

    @app.exception_handler(RequestValidationError)
    async def handle_request_validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Validation failed.",
                "code": "validation_error",
                "errors": normalize_validation_errors(exc.errors()),
            },
        )

    @app.get("/", include_in_schema=False)
    async def root() -> JSONResponse:
        return JSONResponse(
            {
                "name": "Echo API",
                "ui": "Streamlit",
                "run_ui": "streamlit run streamlit_app.py",
            }
        )

    app.include_router(api_router)
    return app


app = create_app()
