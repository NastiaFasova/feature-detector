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
