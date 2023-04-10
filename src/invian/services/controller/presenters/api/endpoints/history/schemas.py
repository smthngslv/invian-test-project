from datetime import datetime

from pydantic import BaseModel, Field

from invian.services.controller.domains.controls.enums import ControlStatus

__all__ = ("HistoryEntry",)


class HistoryEntry(BaseModel):
    start: datetime = Field()
    end: datetime = Field()
    status: ControlStatus = Field()
