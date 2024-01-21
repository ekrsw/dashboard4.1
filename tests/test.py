import os

from apps.models.activity import Activity
from apps.models.support import Support
from apps.models.summary import Summary

import settings

activity_file = os.path.join(settings.FILES_PATH, settings.TS_45DAYS_ACTIVITY_FILE)
support_file = os.path.join(settings.FILES_PATH, settings.TS_45DAYS_SUPPORT_FILE)

activity = Activity(activity_file)
support = Support(support_file)

def run_test(from_date, to_date, group):
    summary = Summary(from_date, to_date, activity, support, group)

    print(f'S11: {summary.row11}')
    print(f'S12: {summary.row12}')
    print(f'S13: {summary.row13}')
    print(f'S14: {summary.row14}')
    print(f'S15: {summary.row15}')
    print(f'S16: {summary.row16}')
    print(f'S17: {summary.row17}')
    print(f'S18: {summary.row18}')
    print(f'S21: {summary.row21}')
    print(f'S23: {summary.row23}')
    print(f'S24: {summary.row24}')
    print(f'S25: {summary.row25}')
    print(f'S26: {summary.row26}')
    print(f'S27: {summary.row27}')
    print(f'S28: {summary.row28}')
    print(f'S29: {summary.row29}')
    print(f'S30: {summary.row30}')
    print(f'S31: {summary.row31}')
    print(f'応答率: {round(summary.response_ratio() * 100, 2)} %')
