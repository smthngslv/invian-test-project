import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

from invian.common import settings
from invian.services.controller.presenters.api.endpoints import router as endpoints
from invian.services.controller.presenters.api.worker import Worker

__all__ = ("application",)

application = FastAPI(
    title="Controller API",
    default_response_class=ORJSONResponse,
    contact={"name": "Ivan Izmailov", "url": "https://t.me/smthngslv", "email": "smthngslv@optic.xyz"},
)

# Allow CORS.
application.add_middleware(
    CORSMiddleware, allow_credentials=True, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
# Allow gzip.
application.add_middleware(GZipMiddleware)

# Include views.
application.include_router(endpoints)

# This is aggregation worker.
worker = Worker(
    tcp_url="tcp://0.0.0.0:1111",
    interval=settings.INTERVAL,
    redis_url=settings.REDIS_URL,
    mongodb_url=settings.MONGODB_URL,
)


@application.on_event("startup")
async def on_startup() -> None:
    application._worker = asyncio.create_task(worker.start())  # type: ignore[attr-defined]


@application.on_event("shutdown")
async def on_shutdown() -> None:
    await worker.shutdown()
    await application._worker  # type: ignore[attr-defined]
