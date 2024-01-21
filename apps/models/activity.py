import datetime as dt
import os
import pandas as pd

from apps.models.serial import datetime_to_serial, serial_to_datetime
import settings

class Activity(object):
    def __init__(self, activity_file=os.path.join(settings.FILES_PATH, settings.TS_TODAYS_ACTIVITY_FILE)):
        # 折返しの計算
        df = pd.read_excel(activity_file)
        self.base_df = df.iloc[:, 3:]
    
    def create_df_by_group(self, from_date, to_date, group):
        df = self.base_df.copy()
        # 件名に「【受付】」が含まれていないもののみ残す
        df['件名'] = df['件名'].astype(str)
        df = df[~df['件名'].str.contains('【受付】', na=False)]

        # from_dateからto_dateの範囲のデータを抽出
        df = self._filtered_by_date_range(df, from_date, to_date)

         # 案件番号でソートし、最も早い日時を残して重複を削除
        df.sort_values(by=['案件番号 (関連) (サポート案件)', '登録日時'], inplace=True)
        df.drop_duplicates(subset='案件番号 (関連) (サポート案件)', keep='first', inplace=True)

        # サポート案件の登録日時と、活動の登録日時をPandas Datetime型に変換して、差分を'時間差'カラムに格納
        df['時間差'] = (df['登録日時'] - df['登録日時 (関連) (サポート案件)'])
        df['時間差'].fillna(0.0, inplace=True)
        
        # 受付タイプが折返しor留守電のものを抽出
        if group != 'HHD':
            df_filtered = df[(df['受付タイプ (関連) (サポート案件)'] == '折返し') | (df['受付タイプ (関連) (サポート案件)'] == '留守電')]
        else:
            df_filtered = df[(df['受付タイプ (関連) (サポート案件)'] == 'HHD入電（折返し）') | (df['受付タイプ (関連) (サポート案件)'] == '留守電')]

        df_group = df_filtered[(df_filtered['サポート区分 (関連) (サポート案件)'] == group)]
        
        self.df_cb_0_20, self.df_cb_20_30, self.df_cb_30_40, self.df_cb_40_60, self.df_cb_60over, self.df_cb_not_include = self._callback_classification_by_group(df_group)

    def _filtered_by_date_range(self, df, from_date, to_date):
        # from_dateからto_dateの範囲のデータを抽出
        from_date_serial = datetime_to_serial(from_date)
        
        to_date_serial = datetime_to_serial(to_date + dt.timedelta(days=1))
        
        df = df[(df['登録日時 (関連) (サポート案件)'] >= from_date_serial) & (df['登録日時 (関連) (サポート案件)'] < to_date_serial)]
        df.reset_index(drop=True, inplace=True)
        return df
    
    def _callback_classification_by_group(self, df):
        towenty_minutes = 0.0138888888888889
        thirty_minutes = 0.0208333333333333
        forty_minutes = 0.0277777777777778
        sixty_minutes = 0.0416666666666667

        df_cb_0_20 = df[(df['時間差'] <= towenty_minutes)]
        df_cb_20_30 = df[(df['時間差'] > towenty_minutes) & (df['時間差'] <= thirty_minutes)]
        df_cb_30_40 = df[(df['時間差'] > thirty_minutes) & (df['時間差'] <= forty_minutes)]
        df_cb_40_60 = df[(df['時間差'] > forty_minutes) & (df['時間差'] <= sixty_minutes) & (df['指標に含めない (関連) (サポート案件)'] == 'いいえ')]
        df_cb_60over = df[(df['時間差'] > sixty_minutes) & (df['指標に含めない (関連) (サポート案件)'] == 'いいえ')]
        df_cb_not_include =df[(df['時間差'] > sixty_minutes) & (df['指標に含めない (関連) (サポート案件)'] == 'はい')]

        return df_cb_0_20, df_cb_20_30, df_cb_30_40, df_cb_40_60, df_cb_60over, df_cb_not_include
    