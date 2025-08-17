"""
Service layer for logging HTTP requests and responses.
This module provides a high-level service for logging API requests, responses,
and file processing activities. It handles JSON parsing, database session management,
and coordinates with the repository layer for persistent storage of log data.
"""
import json
from datetime import datetime
from typing import Optional

from app.core.database import async_session_maker
from app.models.log_request_model import LogRequest
from app.repositories.repositories import LogRequestRepository

class LoggingService:

    def __init__(self):
        self.repository = LogRequestRepository()

    async def log_request_response(self, method: str,
                                   response_body: Optional[str] = None, file_hash: Optional[str] = None) -> Optional[LogRequest]:
        """
                Log an HTTP request with its response data and optional file information.
                Args:
                    method (str): HTTP method used for the request (GET, POST, PUT, DELETE, etc.)
                    response_body (Optional[str]): Raw response body content. Can be JSON string,
                                                 plain text, or None. Defaults to None.
                    file_hash (Optional[str]): Hash identifier of any associated file processing.
                                             Used for linking requests to file operations. Defaults to None.
                Returns:
                    Optional[LogRequest]: The created log entry with generated ID and timestamp,
                                        or None if the operation fails.
                """

        parsed_response = None
        if response_body:
            try:
                parsed_response = json.loads(response_body)
            except json.JSONDecodeError:
                parsed_response = response_body

        log_entry = LogRequest(entry_date=datetime.now(), method=method,
                               response_body=parsed_response, file_hash=file_hash)

        async with async_session_maker() as db:
            return await self.repository.create_request_log(db, log_entry)
