"""
Global feature detector manager with singleton pattern and thread-safe initialization.
"""
import asyncio

from app.utils.feature_detector import FeatureDetector

_detector = None
_ready = False
_lock = asyncio.Lock()

async def get_detector() -> FeatureDetector:
    global _detector, _ready
    if _ready:
        return _detector

    async with _lock:
        if not _ready:
            _detector = FeatureDetector()
            await _detector.warmup()
            _ready = True
    return _detector

async def check_status() -> bool:
    return _ready