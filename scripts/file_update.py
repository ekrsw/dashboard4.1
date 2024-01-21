import os

import settings

from apps.models.excel import Excel

excel = Excel()
excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_ACTIVITY_FILE))
excel.quit()

excel = Excel()
excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_SUPPORT_FILE))
excel.quit()

excel = Excel()
excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_CLOSE_FILE))
excel.quit()