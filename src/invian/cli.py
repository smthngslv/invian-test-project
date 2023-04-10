import importlib.metadata
import os
from argparse import ArgumentParser

from invian.common.utils import start_process

root_cli = ArgumentParser(prog="invian")
root_cli.add_argument("--version", action="version", version=importlib.metadata.version("invian"))

root_subparsers = root_cli.add_subparsers(dest="service")


sensor_cli = root_subparsers.add_parser("sensor")
sensor_cli.add_argument("--concurrency", type=int, default=32)

root_subparsers.add_parser("controller")
root_subparsers.add_parser("manipulator")


def cli() -> None:
    args = root_cli.parse_args()

    if args.service is None:
        root_cli.print_help()
        return

    if args.service == "sensor":
        start_process(f"python -m invian.services.sensor.presenters {args.concurrency}")
        return

    if args.service == "controller":
        start_process(
            f"gunicorn invian.services.controller.presenters.api.application:application --workers {os.cpu_count()} "
            "--worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
        )
        start_process(f"python -m invian.services.sensor {args.concurrency}")
        return

    if args.service == "manipulator":
        start_process("python -m invian.services.manipulator")
        return
