import logging
import os
from datetime import datetime

def get_logger(name: str = "rpa") -> logging.Logger:
    log = logging.getLogger(name)
    if log.handlers:
        return log
    log.setLevel(os.environ.get("LOG_LEVEL", "INFO").upper())
    fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", f"run-{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    log.addHandler(fh)
    log.addHandler(sh)
    return log
