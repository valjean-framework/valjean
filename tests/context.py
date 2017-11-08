import logging
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import valjean  # noqa: F401
valjean.set_log_level(logging.WARNING)
