import logging
import math

from apps.models.reporter import Reporter
import settings

logger = logging.getLogger(__name__)

class Summary(object):
    def __init__(self, from_date, to_date, activity, support, operator, waiting_for_callback, group):
        activity.create_df_by_group(from_date, to_date, group)
        support.create_df_direct_by_group(from_date, to_date, group)
        support.create_df_ivr_by_group(from_date, to_date, group)
        operator.create_df_by_group(from_date, to_date)
        waiting_for_callback.create_df_by_group(from_date, to_date, group)

        # wfc.create_df_wfc_by_group(from_date, to_date, group)
        reporter = Reporter(from_date, to_date, group)

        df_cb_0_20 = activity.df_cb_0_20
        df_cb_20_30 = activity.df_cb_20_30
        df_cb_30_40 = activity.df_cb_30_40
        df_cb_40_60 = activity.df_cb_40_60
        df_cb_60over = activity.df_cb_60over
        df_tb_not_include = activity.df_cb_not_include

        self.row11 = reporter.total_incomming_calls
        self.row12 = reporter.total_abandoned_calls + reporter.total_IVR_disconnected_calls
        self.row14 = reporter.acd_abandoned_calls
        self.row15 = reporter.timeout_calls - support.df_ivr.shape[0]
        self.row13 = self.row14 + self.row15
        self.row16 = support.df_ivr.shape[0]
        self.row17 = self.row11 - self.row12 - self.row13
        self.row18 = self.row16 + self.row17
        self.row21 = support.df_direct.shape[0]
        self.row23 = df_cb_0_20.shape[0]
        self.row24 = self.row21 + self.row23
        self.row25 = df_cb_20_30.shape[0]
        self.row26 = self.row24 + self.row25
        self.row27 = df_cb_30_40.shape[0]
        self.row28 = self.row26 + self.row27
        self.row29 = df_cb_40_60.shape[0]
        self.row30 = self.row28 + self.row29
        self.row31 = df_cb_60over.shape[0]

        self.count_20min_over = waiting_for_callback.c_20over
        self.count_30min_over = waiting_for_callback.c_30over
        self.count_40min_over = waiting_for_callback.c_40over
        self.count_60min_over = waiting_for_callback.c_60over

        # 総着信数
        self.total_incomming_calls = self.row11
        # 電話問い合わせ件数
        self.total_phone_inquiries = self.row18
        # グループ全体のACW, ATT, CPH
        self.acw = operator.acw
        self.att = operator.att
        self.cph = operator.cph
        # 個人別パフォーマンスのDataFrame
        df = operator.df
        self.df = df[df['氏名'] != '合計'].reset_index(drop=True)
    
    def _create_ratio(self, a, b, to_percent, ndigits):
        if b != 0:
            ratio = a / b
        else:
            ratio = 0.0
        
        if to_percent:
            return round(ratio * 100, ndigits)
        else:
            return ratio

    def response_ratio(self, to_percent=False, ndigits=2):
        """応答率
        args:
            to_percent: Trueならパーセント表記にする
            ndigits: パーセント表記の場合の小数点以下の桁数"""
        
        return self._create_ratio(self.row17, self.row11, to_percent, ndigits)

    def direct_ratio(self, to_percent=False, ndigits=2):
        """直受け率
        args:
            to_percent: Trueならパーセント表記にする
            ndigits: パーセント表記の場合の小数点以下の桁数"""
        
        return self._create_ratio(self.row21, self.row18, to_percent, ndigits)
        
    def callback_ratio(self, minutes, to_percent=False, ndigits=2):
        """折返し率
        args:
            minutes: 20, 30, 40のいずれかを指定する
            to_percent: Trueならパーセント表記にする
            ndigits: パーセント表記の場合の小数点以下の桁数"""

        if minutes == 20:
            b = self.row30 + self.row31 + self.count_20min_over
            return self._create_ratio(self.row24, b, to_percent, ndigits)
        elif minutes == 30:
            b = self.row30 + self.row31 + self.count_30min_over
            return self._create_ratio(self.row26, b, to_percent, ndigits)
        elif minutes == 40:
            b = self.row30 + self.row31 + self.count_40min_over
            return self._create_ratio(self.row28, b, to_percent, ndigits)
        else:
            logger.error('minutes must be 20, 30 or 40')
            raise ValueError('minutes must be 20, 30 or 40')

    def get_buffer(self, minutes, group='TVS') -> int:
        """バッファ数
        args:
            minutes: 20, 40のいずれかを指定する"""
        
        if minutes == 0:
            r = settings.KPI_DIRECT_RATIO_TVS
            c = self.row18
            n = self.row21
        elif minutes == 20:
            r = settings.KPI_CALLBACK_RATIO_20MIN_TVS
            c = self.row30 + self.row31 + self.count_20min_over
            n = self.row24
        elif minutes == 30:
            r = settings.KPI_CALLBACK_RATIO_30MIN_TVS
        elif minutes == 40:
            r = settings.KPI_CALLBACK_RATIO_40MIN_TVS
            c = self.row30 + self.row31 + self.count_40min_over
            n = self.row28
        else:
            logger.error('minutes must be 0, 20, 30 or 40')
            raise ValueError('minutes must be 0, 20 or 40')
        
        return self._get_buffer(r, n, c)
        
    def _get_buffer(self, r, n, c) -> int:
        """KPIを達成するためのBufferを計算
        
        args:
            r: KPIの目標値
            n: 現在の達成件数
            c: 分母"""
        
        # KPIを達成できている場合は単純計算、できていない場合少し複雑。
        if c == 0:
            return '-'
        elif n / c >= r:
            b = (n / r) - c
            return int(math.floor(b))
        else:
            b = (n - c * r) / (1 - r)
            return int(math.floor(b))
        