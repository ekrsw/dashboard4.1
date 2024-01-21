import datetime as dt
import os
import string

from apps.views.base_view import View

import settings

class MonitorView(View):
    def __init__(self, summary, template=settings.TEMPLATE_HTML_MONITOR, time_stamp=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        super().__init__(summary, template, time_stamp)
        self.export_path = settings.EXPORT_MONITOR

    def get(self):
        # モニター用テンプレートの読込み
        with open(self.template, 'r') as template_file:
            t_monitor = string.Template(template_file.read())
        
        self.html = t_monitor.substitute(formatten_datetime=self.time_stamp,
                                dep_acw=self.__convert_time_format(self.summary.acw),
                                dep_cph=self.summary.cph,
                                response_ratio =self.summary.response_ratio(True, 1),
                                direct_ratio=self.summary.direct_ratio(True, 1),
                                callback_ratio_20min=self.summary.callback_ratio(20, True, 1),
                                callback_ratio_40min=self.summary.callback_ratio(40, True, 1)
                                )
    
    def __convert_time_format(self, time_str) -> str:
        """hh:mm:ss 形式の時間をmm:ss 形式に変換する関数"""

        t = dt.datetime.strptime(time_str, "%H:%M:%S")
        return t.strftime("%M:%S")
