import os

from apps.models.activity import Activity
from apps.models.operator import Operator
from apps.models.support import Support
from apps.models.summary import Summary
from apps.models.waiting_for_callback import WaitingForCallback

import settings

activity_file = os.path.join(settings.FILES_PATH, settings.TS_45DAYS_ACTIVITY_FILE)
support_file = os.path.join(settings.FILES_PATH, settings.TS_45DAYS_SUPPORT_FILE)
close_file = os.path.join(settings.FILES_PATH, settings.TS_45DAYS_CLOSE_FILE)

activity = Activity(activity_file)
support = Support(support_file)
operator = Operator(close_file)
wfc = WaitingForCallback(activity)

def run_test(from_date, to_date, group):
    summary = Summary(from_date, to_date, activity, support, operator, wfc, group)

    print(f'row11: {summary.row11}')
    print(f'row12: {summary.row12}')
    print(f'row13: {summary.row13}')
    print(f'row14: {summary.row14}')
    print(f'row15: {summary.row15}')
    print(f'row16: {summary.row16}')
    print(f'row17: {summary.row17}')
    print(f'row18: {summary.row18}')
    print(f'row21: {summary.row21}')
    print(f'row23: {summary.row23}')
    print(f'row24: {summary.row24}')
    print(f'row25: {summary.row25}')
    print(f'row26: {summary.row26}')
    print(f'row27: {summary.row27}')
    print(f'row28: {summary.row28}')
    print(f'row29: {summary.row29}')
    print(f'row30: {summary.row30}')
    print(f'row31: {summary.row31}')
    print(f'応答率: {round(summary.response_ratio() * 100, 2)} %')
