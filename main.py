import datetime as dt
import logging
import os
import time

import settings

logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOGLEVEL)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    from apps.models.excel import Excel
    from apps.controller.dashboard import run_today_dashboard

    while True:
        excel = Excel()
        excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_ACTIVITY_FILE))
        excel.quit()

        excel = Excel()
        excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_SUPPORT_FILE))
        excel.quit()

        excel = Excel()
        excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_CLOSE_FILE))
        excel.quit()
        
        run_today_dashboard()
        print('次回更新まで待機中...')
        time.sleep(settings.REFRESH_INTERVAL)

