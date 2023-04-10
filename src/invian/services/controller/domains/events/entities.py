from datetime import datetime as DateTime  # noqa: N812

from pydantic import Field, ValidationError, validator
from pydantic.dataclasses import dataclass
from pydantic.error_wrappers import ErrorWrapper


@dataclass
class EventEntity:
    datetime: DateTime = Field()
    payload: int = Field()

    @validator("datetime")
    def validate_datetime(cls, value: DateTime) -> DateTime:
        if value.tzinfo is None:
            message = "You should specify timezone."
            raise ValidationError(
                [ErrorWrapper(ValueError(message), "datetime")], EventEntity  # type: ignore[arg-type]
            )

        return value
