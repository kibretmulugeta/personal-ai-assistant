"""
Structured logging module.
Configures python standard logging and optional structlog to output formatted JSON or colored logs.
"""

import logging
import sys
from typing import Any, Dict

try:
    import structlog
    HAS_STRUCTLOG = True
except ImportError:
    HAS_STRUCTLOG = False


class StandardJsonFormatter(logging.Formatter):
    """Fallback JSON log formatter using standard logging library."""

    def format(self, record: logging.LogRecord) -> str:
        import json
        from datetime import datetime

        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


def setup_logging(log_level: str = "INFO", is_dev: bool = True) -> None:
    """Configures structured logging for the application."""
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    if HAS_STRUCTLOG:
        shared_processors = [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
        ]
        renderer = structlog.dev.ConsoleRenderer(colors=True) if is_dev else structlog.processors.JSONRenderer()
        structlog.configure(
            processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
        formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=shared_processors,
            processors=[structlog.stdlib.ProcessorFormatter.remove_processors_meta, renderer],
        )
    else:
        if is_dev:
            formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s]: %(message)s")
        else:
            formatter = StandardJsonFormatter()

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(numeric_level)

    for logger_name in ("uvicorn", "uvicorn.access", "sqlalchemy.engine", "asyncpg"):
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Returns a structured logger instance for a given module name."""
    if HAS_STRUCTLOG:
        return structlog.get_logger(name)
    return logging.getLogger(name)
