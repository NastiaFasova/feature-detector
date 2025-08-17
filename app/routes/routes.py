"""
FastAPI router for image processing endpoints.
This module defines HTTP endpoints for image processing operations, including
file upload processing and system status checking. It uses dependency injection
for service layer components.
"""
from fastapi import UploadFile, File, Depends, APIRouter

from app.repositories.repositories import LogRequestRepository
from app.services.process_image_service import ProcessImageService, get_file_hasher, get_request_log_repository
from app.utils.feature_detector_manager import check_status as check_detector_status
from app.utils.file_hash import FileHash

router = APIRouter()

def get_process_image_service(
    file_hasher: FileHash = Depends(get_file_hasher),
    log_repository: LogRequestRepository = Depends(get_request_log_repository),
) -> ProcessImageService:
    return ProcessImageService(file_hasher, log_repository)

@router.post("/process-image")
async def process_image(file: UploadFile = File(...),
                        service: ProcessImageService = Depends(get_process_image_service)):
    """
        Process an uploaded image file.
        Note:
            The endpoint supports caching - identical files (same hash) will
            return cached results without reprocessing.
    """
    result = await service.process_image(file)
    return result

@router.get("/check-status")
async def check_status():
    """
        Check the status of feature-detector.warmup().
    """
    status = await check_detector_status()
    return status
