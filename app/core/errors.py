from fastapi import Request
from fastapi.responses import JSONResponse


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"status": "error", "message": message}
    )


async def validation_exception_handler(request: Request, exc: Exception):
    return error_response(str(exc), 400)


async def general_exception_handler(request: Request, exc: Exception):
    return error_response("Internal server error", 500)

