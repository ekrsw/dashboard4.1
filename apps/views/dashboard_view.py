import os
import string
import datetime as dt

from apps.views.base_view import View

import settings

class DashboardView(View):
    def __init__(self, summary, template=settings.TEMPLATE_HTML, time_stamp=f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 現在"):
        super().__init__(summary, template, time_stamp)
        self.export_path = settings.EXPORT_DASHBOARD

    def get(self):
        # テンプレート読み込み
        with open(self.template, 'r') as template_file:
            html_temp = string.Template(template_file.read())
        self.html = html_temp.substitute(
            formatten_datetime=self.time_stamp,
            acw=self.summary.acw,
            cph=self.summary.cph,
            total_phone_inquiries=self.summary.row18,
            response_ratio=self.summary.response_ratio(to_percent=True),
            response=self.summary.row17,
            response_den=self.summary.row11,
            direct_ratio=self.summary.direct_ratio(to_percent=True),
            direct_calls=self.summary.row21,
            direct_den=self.summary.row18,
            direct_buffer=self.summary.get_buffer(0),
            callback_ratio_20min=self.summary.callback_ratio(20, to_percent=True),
            callback_counts_20min=self.summary.row24,
            callback_den_20min=self.summary.row30 + self.summary.row31 + self.summary.count_20min_over,
            wfc_20over=self.summary.count_20min_over,
            callback_20min_buffer=self.summary.get_buffer(20),
            callback_ratio_30min=self.summary.callback_ratio(30, to_percent=True),
            callback_counts_30min=self.summary.row26,
            callback_den_30min=self.summary.row30 + self.summary.row31 + self.summary.count_30min_over,
            wfc_30over=self.summary.count_30min_over,
            callback_ratio_40min=self.summary.callback_ratio(40, to_percent=True),
            callback_counts_40min=self.summary.row28,
            callback_den_40min=self.summary.row30 + self.summary.row31 + self.summary.count_40min_over,
            wfc_40over=self.summary.count_40min_over,
            callback_40min_buffer=self.summary.get_buffer(40)
        )
