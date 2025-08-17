"""
Repository layer for managing LogRequest database operations.

This module provides a data access layer for LogRequest entities, handling
database operations such as creating log entries and retrieving processing
results by file hash. It follows the repository pattern for clean separation
of concerns between business logic and data access.
"""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.log_request_model import LogRequest


class LogRequestRepository:

    async def create_request_log(self, db: AsyncSession, log_request: LogRequest) -> LogRequest:
        """
                Create a new request log entry in the database.
                Args:
                    db (AsyncSession): Active database session for the transaction
                    log_request (LogRequest): LogRequest object containing method, response_body,
                                            and file_hash data
                Returns:
                    LogRequest: The persisted log entry with generated ID and timestamp

        """
        db_log_request = LogRequest(entry_date=datetime.now(), method=log_request.method,
                                       response_body=log_request.response_body, file_hash=log_request.file_hash)
        db.add(db_log_request)
        await db.commit()
        await db.refresh(db_log_request)
        return db_log_request

    async def get_image_processing_result(self, db: AsyncSession, file_hash: str) -> str | None:
        """
        Searches for a previous processing result using the file hash as a unique
        identifier. This enables caching of expensive image processing operations
        by avoiding re-processing of identical files.

        Args:
            db (AsyncSession): Active database session for the query
            file_hash (str): Unique hash identifier of the processed file

        Returns:
            str | None: The cached response_body data if found, None if no match
                       exists or if an error occurs during retrieval

        Raises:
            Catches all exceptions internally and returns None on error,
            logging the error message to console for debugging.

        Note:
            This method assumes file_hash values are unique per processing result.
            Multiple entries with the same file_hash will return only the first match.
        """
        try:
            stmt = select(LogRequest).where(LogRequest.file_hash == file_hash)
            result = await db.execute(stmt)
            log_request = result.scalars().first()

            if log_request:
                return log_request.response_body
            return None

        except Exception as e:
            print(f"Error fetching result for hash {file_hash}: {e}")
            return None
