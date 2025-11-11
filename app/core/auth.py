from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import API_KEY


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/"):
            api_key = request.headers.get("x-api-key")
            
            if not api_key or api_key != API_KEY:
                raise HTTPException(
                    status_code=401,
                    detail="Unauthorized"
                )
        
        response = await call_next(request)
        return response

