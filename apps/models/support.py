import datetime as dt
import os
import pandas as pd

from apps.models.serial import datetime_to_serial, serial_to_datetime
import settings

class Support(object):
    def __init__(self, support_file=os.path.join(settings.FILES_PATH, settings.TS_TODAYS_SUPPORT_FILE)):
         # ファイルの読み込み
        df_base = pd.read_excel(support_file)
        df_base = df_base.iloc[:, 3:].fillna('')

        # 直受けの検索条件
        df = df_base.copy()
        df = df[(df['受付タイプ'] == '直受け') | (df['受付タイプ'] == 'HHD入電（直受け）')]
        df = df[(df['顛末コード'] != '折返し不要・ｷｬﾝｾﾙ')]
        df = df[(df['顛末コード'] != 'ﾒｰﾙ・FAX回答（送信）')]
        df = df[(df['顛末コード'] != 'SRB投稿（要望）')]
        df = df[(df['顛末コード'] != 'ﾒｰﾙ・FAX文書（受信）')]
        df = df[(df['かんたん！保守区分'] == '会員') | (df['かんたん！保守区分'] == '')]
        df = df[(df['回答タイプ'] != '2次T転送')]
        self.df_direct_base = df

        # 留守電の検索条件
        df = df_base.copy()
        df = df[df['受付タイプ'] == '留守電']
        df = df[(df['顛末コード'] != '折返し不要・ｷｬﾝｾﾙ')]
        df = df[(df['顛末コード'] != 'ﾒｰﾙ・FAX回答（送信）')]
        df = df[(df['顛末コード'] != 'SRB投稿（要望）')]
        df = df[(df['顛末コード'] != 'ﾒｰﾙ・FAX文書（受信）')]
        # Excelの集計ではなぜか対象外になるため追加。含めるためコメントアウト
        # df = df[(df['顛末コード'] != '対応待ち') & (df['顛末コード'] != '対応中')]
        self.df_ivr_base = df
    
    def create_df_direct_by_group(self, from_date, to_date, group):
        # from_dateからto_dateの範囲のデータを抽出
        df = self.df_direct_base.copy()
        df = self._filtered_by_date_range(df, from_date, to_date)
        self.df_direct = df[(df['サポート区分'] == group)]

    def create_df_ivr_by_group(self, from_date, to_date, group):
        # from_dateからto_dateの範囲のデータを抽出
        df = self.df_ivr_base.copy()
        df = self._filtered_by_date_range(df, from_date, to_date)
        self.df_ivr = df[(df['サポート区分'] == group)]
        self.df_ivr.to_excel('ivr.xlsx')

    def _filtered_by_date_range(self, df, from_date, to_date):
        # from_dateからto_dateの範囲のデータを抽出
        from_date_serial = datetime_to_serial(from_date)
        
        to_date_serial = datetime_to_serial(to_date + dt.timedelta(days=1))
        
        df = df[(df['登録日時'] >= from_date_serial) & (df['登録日時'] < to_date_serial)]
        df.reset_index(drop=True, inplace=True)
        return df
