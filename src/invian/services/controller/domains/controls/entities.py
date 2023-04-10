from datetime import datetime as DateTime  # noqa: N812

from pydantic import Field
from pydantic.dataclasses import dataclass

from invian.services.controller.domains.controls.enums import ControlStatus

__all__ = ("ControlEntity",)


@dataclass
class ControlEntity:
    datetime: DateTime = Field()
    status: ControlStatus = Field()
