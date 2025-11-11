from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.auth import AuthMiddleware
from app.core.logger import LoggingMiddleware
from app.core.errors import validation_exception_handler, general_exception_handler
from app.routes.router import api_router

app = FastAPI(title="Utility Service Platform", version="1.0.0")

app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(api_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "healthy"}

