import datetime as dt
import os
import sys

from apps.models.activity import Activity
from apps.models.excel import Excel
from apps.models.support import Support
from apps.models.operator import Operator
from apps.models.summary import Summary
from apps.models.waiting_for_callback import WaitingForCallback

import settings

excel = Excel()
excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_ACTIVITY_FILE))
excel.quit()

excel = Excel()
excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_SUPPORT_FILE))
excel.quit()

excel = Excel()
excel.refresh_save(os.path.join(settings.FILES_PATH, settings.TS_TODAYS_CLOSE_FILE))
excel.quit()

groups = sys.argv[1:]

today = dt.date.today()

activity_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_ACTIVITY_FILE)
support_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_SUPPORT_FILE)
close_file = os.path.join(settings.FILES_PATH, settings.TS_TODAYS_CLOSE_FILE)

activity = Activity(activity_file)
support = Support(support_file)
operator = Operator(close_file)
wfc = WaitingForCallback(activity)

for group in groups:
    summary = Summary(today, today, activity, support, operator, wfc, group)
    print(f'電話問い合わせ件数({group}): {summary.row18}')
    print(f'応答率({group}): {summary.row17} / {summary.row11} {summary.response_ratio(to_percent=True)} %')
    print(f'直受け率({group}): {summary.row21} / {summary.row18} {summary.direct_ratio(to_percent=True)} %')
    print(f'20分以内折返し率({group}): {summary.row24} / {(summary.row30 + summary.row31)} {summary.callback_ratio(20, to_percent=True)} %')
    print(f'30分以内折返し率({group}): {summary.row26} / {(summary.row30 + summary.row31)} {summary.callback_ratio(30, to_percent=True)} %')
    print(f'40分以内折返し率({group}): {summary.row28} / {(summary.row30 + summary.row31)} {summary.callback_ratio(40, to_percent=True)} %')
