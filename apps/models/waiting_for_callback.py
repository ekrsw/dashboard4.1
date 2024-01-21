"""作成中。Ver3.1のPendingDataFrameクラスのコンストラクタをとりあえずコピーしている。"""

import datetime as dt
import logging
import os
import pandas as pd

from apps.models.serial import datetime_to_serial, current_time_to_serial

import settings

logger = logging.getLogger(__name__)

class WaitingForCallback(object):
    def __init__(self, activity):
        self.base_df = activity.base_df.copy()
    
    def create_df_by_group(self, from_date, to_date, group):
        df = self.base_df.copy()
        # サポート案件がgroupと一致するものを抽出。
        df = df[(df['サポート区分 (関連) (サポート案件)'] == group)]

        # 受付けタイプ「直受け」「折返し」「留守電」のみ残す
        df = df[(df['受付タイプ (関連) (サポート案件)'] == '折返し') | (df['受付タイプ (関連) (サポート案件)'] == '留守電')]

        # 指標に含めないが「いいえ」のもののみ残す
        df = df[df['指標に含めない (関連) (サポート案件)'] == 'いいえ']

        df = df[(df['顛末コード (関連) (サポート案件)'] == '対応中') | (df['顛末コード (関連) (サポート案件)'] == '対応待ち')]

        # 件名に「【受付】」が含まれているもののみ残す。
        df['件名'] = df['件名'].astype(str) 
        contains_df = df[df['件名'] == '【受付】']
        uncontains_df = df[df['件名'] != '【受付】']

        only_contains_df = pd.merge(contains_df, uncontains_df, on='案件番号 (関連) (サポート案件)', how='outer', indicator=True)
        result = only_contains_df[only_contains_df['_merge'] == 'left_only']
        s = result['案件番号 (関連) (サポート案件)'].unique()
        df = df[df['案件番号 (関連) (サポート案件)'].isin(s)]

        # 案件番号、登録日時でソート
        df.sort_values(by=['案件番号 (関連) (サポート案件)', '登録日時'], inplace=True)

        # 同一案件番号の最初の活動のみ残して他は削除  
        df.drop_duplicates(subset='案件番号 (関連) (サポート案件)', keep='first', inplace=True)
        
        # サポート案件の登録日時と、活動の登録日時をPandas Datetime型に変換して、差分を'お待たせ時間'カラムに格納、NaNは０変換
        current_serial = current_time_to_serial()
        df['お待たせ時間'] = (current_serial - df['登録日時 (関連) (サポート案件)'])
        df = self.__filtered_by_date_range(df, from_date, to_date)
        df.reset_index(drop=True, inplace=True)
        self.df = df
        if settings.DEBUG:
            self.df.to_excel('wfc_df.xlsx', index=False)
        self.c_20over, self.c_30over, self.c_40over, self.c_60over = self.__convert_to_pending_num(df)
        
    def __filtered_by_date_range(self, df, from_date, to_date):
        # from_dateからto_dateの範囲のデータを抽出
        from_date_serial = datetime_to_serial(from_date)
        to_date_serial = datetime_to_serial(to_date + dt.timedelta(days=1))
        
        df = df[(df['登録日時 (関連) (サポート案件)'] >= from_date_serial) & (df['登録日時 (関連) (サポート案件)'] < to_date_serial)]
        df.reset_index(drop=True, inplace=True)
        return df
    
    def __convert_to_pending_num(self, df):
        towenty_minutes = 0.0138888888888889
        thirty_minutes = 0.0208333333333333
        forty_minutes = 0.0277777777777778
        sixty_minutes = 0.0416666666666667

        df_20over = df[df['お待たせ時間'] >= towenty_minutes]
        df_30over = df[df['お待たせ時間'] >= thirty_minutes]
        df_40over = df[df['お待たせ時間'] >= forty_minutes]
        df_60over = df[df['お待たせ時間'] >= sixty_minutes]

        c_20over = df_20over.shape[0]
        c_30over = df_30over.shape[0]
        c_40over = df_40over.shape[0]
        c_60over = df_60over.shape[0]

        return c_20over, c_30over, c_40over, c_60over

    