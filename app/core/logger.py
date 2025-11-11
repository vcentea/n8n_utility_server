import logging
import json
import time
from datetime import datetime
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import LOG_LEVEL


logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
    format="%(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        response = await call_next(request)
        
        duration_ms = round((time.time() - start_time) * 1000, 2)
        
        log_data = {
            "time": datetime.utcnow().isoformat() + "Z",
            "level": "info",
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": duration_ms
        }
        
        logger.info(json.dumps(log_data))
        
        return response

