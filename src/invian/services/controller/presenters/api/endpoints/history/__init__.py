from fastapi import APIRouter

__all__ = ("router",)

router = APIRouter(prefix="/history")

import invian.services.controller.presenters.api.endpoints.history.view  # noqa: F401, E402
