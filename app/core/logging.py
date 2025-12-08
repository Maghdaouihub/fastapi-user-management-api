"""
Logging configuration module
Provides structured logging setup for the application
"""
import logging
import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.
    Intercepts standard logging messages toward loguru sinks.
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    """Configure logging for the application"""

    # Remove default logger
    logger.remove()

    # Add console logger
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="DEBUG" if settings.DEBUG else "INFO",
        colorize=True,
    )

    # Add file logger
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)

    logger.add(
        log_path / "app.log",
        rotation="500 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    # Intercept uvicorn logs
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"]:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]

    logger.info("Logging configured successfully")
