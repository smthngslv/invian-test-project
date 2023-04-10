from datetime import datetime, timezone

__all__ = ("round_to_interval",)


def round_to_interval(date: datetime, interval: int) -> datetime:
    return datetime.fromtimestamp(int(date.timestamp() // interval * interval), tz=timezone.utc)
