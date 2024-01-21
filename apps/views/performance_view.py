import datetime as dt
import string

from apps.views.base_view import View

import settings

class PerformanceView(View):
    def __init__(self, summary, template=settings.TEMPLATE_HTML_PERFORMANCE, time_stamp=f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 現在"):
        super().__init__(summary, template, time_stamp)
        self.export_path = settings.EXPORT_PERFORMANCE
        table = self.summary.df.to_html(index=False, classes='styled-table')
        table = table.replace(' style="text-align: right;"', '')
        self.html_table = table.replace('dataframe styled-table', 'styled-table')

    def get(self):
        # パフォーマンス用テンプレートの読み込み
        with open(self.template, 'r') as template_file:
            t = string.Template(template_file.read())
        
        self.html = t.substitute(formatten_datetime=self.time_stamp,
                                 html_table=self.html_table)
