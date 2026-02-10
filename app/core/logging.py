import logging
from rich.logging import RichHandler


def setup_logging():

    logging.basicConfig(
        level = logging.INFO,
        format = "%(message)s",
        datefmt = "[%X]",
        handlers = [
            RichHandler(
                rich_tracebacks=True,
                tracebacks_show_locals=False
            )
        ],
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)