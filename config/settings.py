import configparser
from typing import Optional

config = configparser.ConfigParser()

config.read('config\settings.ini')

# Loging
LOG_DIR: Optional[str] = config.get('Loging', 'LOG_DIR', fallback=None)

# Advertising
SEND_INTERVAL_MIN: Optional[int] = config.getint('Advertising', 'SEND_INTERVAL_MIN', fallback=None) * 60
USE_AD: Optional[bool] = config.getboolean('Advertising', 'USE_AD', fallback=None)

if LOG_DIR is None or SEND_INTERVAL_MIN is None or USE_AD is None:
    raise ValueError("One or more required keys are missing in the settings.ini file.")
