import logging
from datetime import datetime, date

# Show Log Level
# print(logging.getLevelName(0))    # NOTSET
# print(logging.getLevelName(10))   # DEBUG
# print(logging.getLevelName(20))   # INFO
# print(logging.getLevelName(30))   # WARNING
# print(logging.getLevelName(40))   # ERROR
# print(logging.getLevelName(50))   # CRITICAL

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

log = logging.getLogger(__name__)

# logger = logging.getLogger(__name__)
