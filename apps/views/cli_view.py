import datetime as dt
from apps.models.summary import Summary

def run_today_test(activity, support, groups):
    today = dt.date.today()

    for group in groups:
        summary = Summary(today, today, activity, support, group)
        print(f'総着信数({group}): {summary.row11}')
        print(f'応答率({group}): {round(summary.response_rate() * 100, 2)} %')
        print(f'直受け率({group}): {round(summary.direct_rate() * 100, 2)} %')
        print(f'20分以内折返し率({group}): {round(summary.callback_rate(20) * 100, 2)} %')
        print(f'30分以内折返し率({group}): {round(summary.callback_rate(30) * 100, 2)} %')
        print(f'40分以内折返し率({group}): {round(summary.callback_rate(40) * 100, 2)} %')

def run_test(from_date, to_date, activity, support, groups):
    
    for group in groups:
        summary = Summary(from_date, to_date, activity, support, group)
        print(f'総着信数({group}): {summary.row11}')
        print(f'応答率({group}): {round(summary.response_rate() * 100, 2)} %')
        print(f'直受け率({group}): {round(summary.direct_rate() * 100, 2)} %')
        print(f'20分以内折返し率({group}): {round(summary.callback_rate(20) * 100, 2)} %')
        print(f'30分以内折返し率({group}): {round(summary.callback_rate(30) * 100, 2)} %')
        print(f'40分以内折返し率({group}): {round(summary.callback_rate(40) * 100, 2)} %')