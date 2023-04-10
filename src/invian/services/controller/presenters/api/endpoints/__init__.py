from fastapi import APIRouter

from invian.services.controller.presenters.api.endpoints.events import router as events
from invian.services.controller.presenters.api.endpoints.history import router as history

__all__ = ("router",)

router = APIRouter()

router.include_router(events, prefix="/v1")
router.include_router(history, prefix="/v1")
