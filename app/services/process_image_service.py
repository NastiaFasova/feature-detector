"""
Service layer for image processing operations with caching and feature detection.
"""
import asyncio
import os
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.core.database import async_session_maker
from app.utils.feature_detector_manager import get_detector
from app.repositories.repositories import LogRequestRepository
from app.utils.file_hash import FileHash

def get_file_hasher():
    return FileHash()

def get_request_log_repository():
    return LogRequestRepository()

class ProcessImageService:

    def __init__(self, file_hasher: FileHash, log_repository: LogRequestRepository):
        self.file_hasher = file_hasher
        self.log_repository = log_repository

    async def process_image(self, file: UploadFile):
        """
                The method uses file hashing to implement intelligent caching - identical
                files (same content) will return cached results without reprocessing,
                significantly improving performance and reducing computational overhead.

                Args:
                    file (UploadFile): FastAPI UploadFile object containing the image data.
                                     Supports common image formats (JPEG, PNG, etc.)
                """
        content = await file.read()
        await file.seek(0)

        file_hash = await self.file_hasher.calculate_file_hash(content)

        async with async_session_maker() as db:
            result = await self.log_repository.get_image_processing_result(db, file_hash)

        if result is not None:
            return result

        async with aiofiles.tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=Path(file.filename).suffix) as temp_file:
            await temp_file.write(content)
            temp_path = temp_file.name

        try:
            detector = await get_detector()
            result = await detector.process_image(temp_path)
            return result
        finally:
            await asyncio.to_thread(os.remove, temp_path)
