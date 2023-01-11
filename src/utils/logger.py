import logging as LOG
import os

log_level = os.getenv("LOGLEVEL", "INFO")
LOG.basicConfig(level=log_level)
