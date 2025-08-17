from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.log_request_model import LogRequest


class LogRequestRepository:

    async def create_request_log(self, db: AsyncSession, log_request: LogRequest) -> LogRequest:
        db_log_request = LogRequest(entry_date=datetime.now(), method=log_request.method,
                                       response_body=log_request.response_body, file_hash=log_request.file_hash)
        db.add(db_log_request)
        await db.commit()
        await db.refresh(db_log_request)
        return db_log_request

    async def get_image_processing_result(self, db: AsyncSession, file_hash: str) -> str | None:
        """Get processing result by file hash"""
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
