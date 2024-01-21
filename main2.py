import datetime as dt
import logging
import os
import time

import settings

logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOGLEVEL)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    from scripts.fetch_kpi import fetch_range

    from_date = dt.date(2024, 1, 1)
    to_date = dt.date(2024, 1, 16)
    
    fetch_range(from_date, to_date, ['TVS'])
