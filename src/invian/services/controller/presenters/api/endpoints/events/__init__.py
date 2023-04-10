from fastapi import APIRouter

__all__ = ("router",)

router = APIRouter(prefix="/events")

import invian.services.controller.presenters.api.endpoints.events.view  # noqa: F401, E402
