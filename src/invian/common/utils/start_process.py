import os
import shlex
import signal
import sys
from subprocess import Popen


def start_process(command: str, *, environment: dict[str, str] | None = None) -> None:
    if environment is None:
        environment = {}

    with Popen(
        shlex.split(command), stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, env={**os.environ, **environment}
    ) as process:
        signal.signal(signal.SIGTERM, lambda s, _: process.send_signal(s))

        while True:
            try:
                sys.exit(process.wait())

            except KeyboardInterrupt:
                continue
