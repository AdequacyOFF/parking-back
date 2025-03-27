from __future__ import annotations

import logging
import sys
from types import FrameType
from typing import Callable

import loguru
import orjson

from app.settings import LoggingSettings


class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/health") == -1


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        loglevel_mapping = {
            50: "CRITICAL",
            40: "ERROR",
            30: "WARNING",
            20: "INFO",
            10: "DEBUG",
            0: "NOTSET",
        }
        try:
            level: str | int = loguru.logger.level(record.levelname).name
        except ValueError:
            level = loglevel_mapping[record.levelno]

        # Find caller from where originated the logged message
        frame: FrameType | None
        frame, depth = logging.currentframe(), 2
        while frame is not None and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        loguru.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _json_sink_wrapper() -> Callable[[loguru.Message], None]:
    def _json_sink(message: loguru.Message) -> None:
        record = message.record
        exception_ = record["exception"]
        exception = exception_ and {
            "type": None if exception_.type is None else exception_.type.__name__,
            "value": exception_.value,
            "traceback": bool(exception_.traceback),
        }
        serializable = {
            "level": record["level"].name,
            "message": record["message"],
            "extra": record["extra"],
            "exception": exception,
            "function": record["function"],
            "line": record["line"],
            "module": record["module"],
            "name": record["name"],
            "time": {"repr": record["time"], "timestamp": record["time"].timestamp()},
            "elapsed": {
                "repr": record["elapsed"],
                "seconds": record["elapsed"].total_seconds(),
            },
            "level_no": record["level"].no,
        }
        sys.stdout.write(
            orjson.dumps(
                serializable,
                default=str,
                option=orjson.OPT_APPEND_NEWLINE | orjson.OPT_NON_STR_KEYS,
            ).decode()
        )

    return _json_sink


def setup_logging(
    settings: LoggingSettings,
) -> None:
    # Disabling uvicorn logs
    loggers = (logging.getLogger(name) for name in logging.root.manager.loggerDict if name.startswith("uvicorn"))
    for uvicorn_logger in loggers:
        uvicorn_logger.addFilter(HealthCheckFilter())
    # Setup logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    loguru_handlers = []

    if settings.json_enabled:
        loguru_handlers += [
            {
                "sink": _json_sink_wrapper(),
                "colorize": False,
                "level": settings.level,
                "backtrace": False,
                "format": "",
            }
        ]

    else:
        format_ = (
            "<green>{time:YYYY-MM-DDTHH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        if settings.extra_context:
            format_ += " | <level>{extra!s}</level>"

        loguru_handlers += [
            {
                "sink": sys.stdout,
                "level": settings.level,
                "backtrace": False,
                "format": format_,
            },
        ]

    loguru.logger.configure(handlers=loguru_handlers)
