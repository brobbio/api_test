import logging
import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

def create_log_dir():
    default = Path("/var/log/.coingecko/logs")
    if os.access("/var/log", os.W_OK):
        default.mkdir(parents=True, exist_ok=True)
        return str(default)

    local = Path("./logs")
    local.mkdir(parents=True, exist_ok=True)
    return str(local)

def setup_logger():
    '''Logger configuration to rotate daily'''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_file = os.path.join(create_log_dir(),"coingecko.log")
    log_file_path = Path(log_file)

    if not log_file_path.exists():
        log_file_path.touch()

    try:
        #Let users write to log
        os.chmod(log_file_path, 0o666) 
    except PermissionError:
        pass

    handler = TimedRotatingFileHandler(
        log_file,
        when="midnight",
        interval=1,
        backupCount=7
    )

    formatter = logging.Formatter(
        "[%(asctime)s | %(levelname)s] : %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger