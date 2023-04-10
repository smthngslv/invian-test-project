import asyncio
import sys
from contextlib import suppress
from urllib.parse import urlsplit

import msgpack

from invian.common import settings

__all__ = ("tcp_client",)


async def tcp_client(url: str, *, attempts: int = 5) -> None:
    try:
        _, netloc, _, _, _ = urlsplit(url, scheme="tcp")
        host, port = netloc.split(":")

    except Exception as exception:
        print(f"URL should be in the following form: tcp://host:port: {exception}", flush=True)  # noqa: T201
        sys.exit(-1)

    reader = None
    for _attempt in range(attempts):
        with suppress(Exception):
            reader, _ = await asyncio.open_connection(host, port)
            break

    if reader is None:
        print(f"Cannot connect to {host}:{port}.", flush=True)  # noqa: T201
        sys.exit(-1)

    # Success.
    print(f"Connected to {host}:{port}.", flush=True)  # noqa: T201

    buffer = b""
    while True:
        data = await reader.read(1)

        # Connection close.
        if len(data) == 0:
            break

        buffer += data

        # If we received complete package.
        if buffer[-4:] == b"\00\00\00\00":
            print(msgpack.unpackb(buffer[:-4]), flush=True)  # noqa: T201

            # Clear buffer.
            buffer = b""


if __name__ == "__main__":
    asyncio.run(tcp_client(settings.CONTROLLER_TCP_URL))
