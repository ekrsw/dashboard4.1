import datetime as dt

from apps.models.summary import Summary
from apps.models.activity import Activity
from apps.models.support import Support

today = dt.date.today()
activity = Activity('TS_todays_activity.xlsx')
support = Support('TS_todays_support.xlsx')
def test_to_html(group):
    
    summary = Summary(today, today, activity, support, group)

    total_incomming_calls = summary.row11
    response_rate = round(summary.response_rate() * 100, 2)
    direct_rate = round(summary.direct_rate() * 100, 2)
    callback_within_20min_rate = round(summary.callback_rate(20) * 100, 2)
    callback_within_30min_rate = round(summary.callback_rate(30) * 100, 2)
    callback_within_40min_rate = round(summary.callback_rate(40) * 100, 2)

    return total_incomming_calls, response_rate, direct_rate, callback_within_20min_rate, callback_within_30min_rate, callback_within_40min_rate

(total_incomming_calls_tvs,
response_rate_tvs,
direct_rate_tvs,
callback_within_20min_rate_tvs,
callback_within_30min_rate_tvs,
callback_within_40min_rate_tvs) = test_to_html('TVS')

(total_incomming_calls_ss,
response_rate_ss,
direct_rate_ss,
callback_within_20min_rate_ss,
callback_within_30min_rate_ss,
callback_within_40min_rate_ss) = test_to_html('SS')

(total_incomming_calls_kmn,
response_rate_kmn,
direct_rate_kmn,
callback_within_20min_rate_kmn,
callback_within_30min_rate_kmn,
callback_within_40min_rate_kmn) = test_to_html('顧問先ソフトウェア')

(total_incomming_calls_hhd,
response_rate_hhd,
direct_rate_hhd,
callback_within_20min_rate_hhd,
callback_within_30min_rate_hhd,
callback_within_40min_rate_hhd) = test_to_html('HHD')
