import datetime as dt
import logging
import os
import pandas as pd

import settings

logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOGLEVEL)
logger = logging.getLogger(__name__)

class Shift(object):
    def __init__(self, member_df):

        date_str = dt.date.today().strftime("%d")
        shift_file = settings.SHIFT_FILE

        # CSVファイルを読み込む。ヘッダーは3行目（0-indexed）にある。
        if os.path.exists(shift_file):
            df = pd.read_csv(shift_file, skiprows=2, header=1, index_col=1, quotechar='"', encoding='shift_jis')
            # 最後の1列を削除
            df = df.iloc[:, :-1]
            # "組織名"、"従業員ID"、"種別" の列を削除
            df = df.drop(columns=["組織名", "従業員ID", "種別"])
            df = df[[date_str]]
            df.columns = ['シフト']

            # メンバーリストのファイルから、シフトのファイルにある名前を正式な氏名のフォーマットに変換
            df.index = df.index.map(member_df.set_index('Sweet')['氏名'].to_dict())
        else:
            logger.error(f"File not found: {shift_file}")
            raise FileNotFoundError(f"File not found: {shift_file}")

        self.shift_df = df