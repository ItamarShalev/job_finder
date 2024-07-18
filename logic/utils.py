import logging
from pathlib import Path

from dotenv import load_dotenv


def get_logger(level=logging.DEBUG) -> logging.Logger:
    format_logging = "%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(message)s"
    handlers = [logging.StreamHandler()]
    logging.basicConfig(handlers=handlers, datefmt="%H:%M:%S", level=level, format=format_logging)
    return logging.getLogger(__package__)


def load_environment_variables():
    load_dotenv(get_main_project_folder() / ".env")


def get_main_project_folder() -> Path:
    return Path(__file__).parent.parent
