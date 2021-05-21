import os
import logging
from decimal import Decimal

from decouple import config

LOG_LEVEL = getattr(
    logging, config("LOG_LEVEL", default="INFO", cast=str).upper(), logging.INFO
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=LOG_LEVEL,
)

FILE_DIR = os.path.join(os.getcwd(), "files")
FILE_INPUT = os.path.join(FILE_DIR, "input.txt")
FILE_OUTPUT = os.path.join(FILE_DIR, "output.txt")

TICK_COST = Decimal("1")
