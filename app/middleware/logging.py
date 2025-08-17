import asyncio

from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.services.logging_service import LoggingService
from app.utils.file_hash import FileHash


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware class that extends BaseHTTPMiddleware.
    This properly handles request/response logging.
    """
    def __init__(self, app):
        super().__init__(app)
        self.logging_service = LoggingService()
        self.file_hash = FileHash()

    async def dispatch(self, request: Request, call_next):
        """
        Main middleware method - called for every HTTP request.

        Args:
            request: The incoming request
            call_next: Function to call the next middleware or endpoint
        """
        file_hash = await self._extract_file_hash_safely(request)

        response = await call_next(request)

        response_body = await self._extract_response_body(response)

        asyncio.create_task(
            self.logging_service.log_request_response(
                method=str(request.url.path),
                response_body=response_body,
                file_hash=file_hash
            )
        )

        return response

    async def _extract_file_hash_safely(self, request: Request) -> str:
        """Extract file hash without consuming the request body permanently"""
        try:
            body = await request.body()

            async def receive():
                return {
                    "type": "http.request",
                    "body": body,
                    "more_body": False
                }

            request._receive = receive

            return await self.file_hash.extract_file_hash_from_request(request)

        except Exception as e:
            print(f"Error extracting file hash in middleware: {e}")
            return ""

    async def _extract_response_body(self, response: Response) -> str:
        """Extract response body without breaking the response"""
        try:
            body_chunks = []
            async for chunk in response.body_iterator:
                body_chunks.append(chunk)

            response.body_iterator = iterate_in_threadpool(iter(body_chunks))

            body_bytes = b"".join(body_chunks)
            try:
                return body_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return f"<binary data: {len(body_bytes)} bytes>"

        except Exception as e:
            return "<error extracting response>"