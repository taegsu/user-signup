from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from pydantic import ValidationError

from app.common.database.postgres.manage import init_database
from app.router.user_api import router as api_router


def create_app():
    app = FastAPI(
        title="User Sign Up API",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        now = datetime.now()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "description": "Internal Server Error",
                "timestamp": now.isoformat(),
                "path": request.url.path,
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"title": "HTTP Error", "description": exc.detail}
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
        loc = exc.errors()[0]["loc"]
        msg = exc.errors()[0]["msg"]
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"title": "Validation Error", "description": msg, "loc": loc},
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        loc = exc.errors()[0]["loc"]
        msg = exc.errors()[0]["msg"]
        title = "invalid"
        if msg == "field required":
            missing_field = loc[-1]
            title = missing_field + ":drop"
            msg = missing_field + " 없음"
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"title": title, "description": msg, "loc": loc},
        )

    return app


app = create_app()
