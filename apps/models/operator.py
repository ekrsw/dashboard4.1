import datetime as dt
import numpy as np
import pandas as pd

from apps.models.member import Member
from apps.models.reporter import OperatorAnalysis
from apps.models.shift import Shift
import settings

class Operator(object):
    def __init__(self, closefile):
        # クローズ、メンバー、シフトのデータを読み込む
        self._close_df = pd.read_excel(closefile)
        self._member_df = Member().member_df
        self._shift_df = Shift(self._member_df).shift_df
    
    def create_df_by_group(self, from_date, to_date):
        """from_dateからto_dateの範囲でレポータをスクレイピングし、KPIを計算してDataFrameを作成する。
        Args:
            from_date(datetime.date): 開始日
            to_date(datetime.date): 終了日"""

        # from_dateからto_dateの範囲でレポータをスクレイピング
        df = self.__load_reporter(from_date, to_date)

        # メンバーリストを読込み、レポータの名前を正式な氏名のフォーマットに変換。氏名をインデックスに設定。
        renamed_df = self.__convert_reporter_names(df, self._member_df)
        renamed_df.rename_axis('氏名', inplace=True)

        # hh:mm:ss 形式の時間を1日を1としたときの時間に変換
        renamed_df = renamed_df.applymap(self.__time_to_days)

        close_df = self._close_df.copy()
        close_df = self.__load_closefile(close_df, from_date, to_date)

        # レポータのスクレイピング結果とクローズファイルをjoin
        join_df = renamed_df.join(close_df, how='left').fillna(0)
        kpi_df = self.__get_kpi(join_df)
        join_df = kpi_df.join(self._member_df, how='left').fillna('')
        join_df = join_df.join(self._shift_df, how='left').fillna('')
        # シフトが'週休'となっているレコードを削除する。
        join_df = join_df[~((join_df['シフト'] == '週休') & (join_df['クローズ'] == 0))]

        join_df = join_df[['SV', 'シフト', 'ACW', 'ATT', 'CPH', 'クローズ']]
        df = join_df.sort_values(by=['クローズ', 'シフト'], ascending=[False, True])
    
        self.acw = df.loc['合計', 'ACW']
        self.att = df.loc['合計', 'ATT']
        self.cph = df.loc['合計', 'CPH']

        df['氏名'] = df.index
        self.df = df[['氏名', 'SV', 'シフト', 'ACW', 'ATT', 'CPH', 'クローズ']].reset_index(drop=True)

    def __load_reporter(self, from_date, to_date):
        operator_analysis = OperatorAnalysis(from_date, to_date)
        return operator_analysis.df
    
    def __load_closefile(self, df, from_date, to_date):
        
        # 最初の3列をスキップし、5列目をインデックスとして設定します
        df = df.iloc[:, 3:].set_index(df.columns[5])
        df.reset_index(inplace=True)
        df['完了日時'] = pd.to_datetime(df['完了日時'])

        # DataFrameのインデックスを日付でソートする
        df.sort_values(by=['完了日時'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        from_date = pd.to_datetime(from_date)

        # 指定した期間のデータのみ残す。to_dateは翌日の0時までのデータを取得するため、1日加算する
        to_date = pd.to_datetime(to_date) + dt.timedelta(days=1)
        df = df[(df['完了日時'] >= from_date) & (df['完了日時'] < to_date)]
        df.set_index(['所有者'], inplace=True)

        counts = df.index.value_counts()
        df = pd.DataFrame(counts).reset_index()
        df.columns = ['氏名', 'クローズ']
        df = df.set_index(df.columns[0])

        return df

    def __convert_reporter_names(self, df, member_df) -> pd.DataFrame:
        """member_list.xlsxから、レポータの名前を正式な氏名のフォーマットに変換
        Args:
            df(pd.DataFrame): レポータからスクレイピングしたDataFrame
        
        return:
            df(pd.DataFrame): 名前を正式な氏名のフォーマットに変換したDataFrame"""

        index_dict_reporter = member_df.set_index('レポータ')['氏名'].to_dict()
        df.index = df.index.map(index_dict_reporter)
        
        return df
    
    def __create_acw_att_cph_columns(self, df, addition):
        '''スクレイピングした指標から、ACW, ATT, CPHを計算してdfにカラムを追加して返す
        0除算を避けるために、0の場合はいったん1にreplaceしている'''

        
        # 実際の計算
        df['ACW'] = (df['ワークタイムの合計'] + df['着信後処理時間の合計'] + df['発信後処理時間の合計'] + df['事前準備時間の合計'] + df['転送可時間の合計'] + df['一時離席時間の合計']) / df['クローズ'].replace(0, 1)
        df.loc[df['クローズ']==0, 'ACW'] = 0
        df['ATT'] = (df['着信通話時間の合計(外線)'] + df['発信通話時間の合計(外線)']) / df['クローズ'].replace(0, 1)
        df.loc[df['クローズ']==0, 'ATT'] = 0
        
        if addition:
            _tmp = (df['着信通話時間の合計'] + df['発信通話時間の合計'] + df['ワークタイムの合計'] + df['着信後処理時間の合計'] + df['発信後処理時間の合計'] + df['離席時間の合計'] + df['事前準備時間の合計'] + df['一時離席時間の合計']) * 24
        else:
            _tmp = (df['ログオン時間'] - (df['待機時間'] + df['昼休憩時間の合計'] + df['研修/会議時間の合計'] + df['別作業中時間の合計'] + df['他者支援時間の合計'] + df['開発資料確認時間の合計'] + df['資料作成時間の合計'])) * 24
        df['CPH'] = np.where(
            _tmp == 0,
            0,
            df['クローズ'] / _tmp
        )
        
        df = df.replace(np.inf, 0)

        return df
    
    def __get_kpi(self, df, addition=settings.CPH_ADDITION, sum=settings.SUM, hms=settings.HMS, digits=2):
        if sum:
            df.loc['合計'] = df.sum(numeric_only=True)
        kpi_df = self.__create_acw_att_cph_columns(df, addition)
        if hms:
            kpi_df[['ACW','ATT']] = kpi_df[['ACW','ATT']].applymap(self.__float_to_hms)
        kpi_df[['CPH']] = kpi_df[['CPH']].round(digits)
        kpi_df[['クローズ']] = kpi_df[['クローズ']].astype(int)
        return kpi_df[['ACW', 'ATT', 'CPH', 'クローズ']]
    
    def __float_to_hms(self, value) -> str:
        '''1日を1としたfloat型を'hh:mm:ss'形式の文字列に変換'''
    
        # 1日が1なので、24を掛けて時間単位に変換
        hours = value * 24

        # 時間の整数部分
        h = int(hours)

        # 残りの部分を分単位に変換
        minutes = (hours - h) * 60

        # 分の整数部分
        m = int(minutes)

        # 残りの部分を秒単位に変換
        seconds = (minutes - m) * 60

        # 秒の整数部分
        s = int(seconds)

        return f"{h:02}:{m:02}:{s:02}"
    
    def __time_to_days(self, time_str) -> float:
        """hh:mm:ss 形式の時間を1日を1としたときの時間に変換する関数
        Args:
            time_str(str): hh:mm:ss 形式の時間
        
        return:
            float: 1日を1としたときの時間"""
        

        # t = dt.datetime.strptime(time_str, "%H:%M:%S")
        split_time = time_str.split(':')
        t = (float(split_time[0]) + float(split_time[1]) / 60 + float(split_time[2]) / 3600) / 24

        return t
