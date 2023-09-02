import json
import os
from datetime import datetime
from typing import Optional

from utils.io import print_system


LOG_DIR = "logs"

LOGS = {}


def log(skip_stdout: bool = False, **kwargs) -> None:
    LOGS.update(kwargs)
    if not skip_stdout:
        for k, w in kwargs.items():
            print_system(f"{k}: {w}")


def dump() -> None:
    _check_directory()

    now = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
    log_file = f"{LOG_DIR}/{now}.json"

    with open(log_file, "w") as f:
        f.write(json.dumps(LOGS, indent="\t"))


def _check_directory() -> None:
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
