import logging
import os
import time
import win32com.client as win32

import settings

logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOGLEVEL)
logger = logging.getLogger(__name__)

class Excel(object):
    def __init__(self):
        self.excel = win32.gencache.EnsureDispatch('Excel.Application')
        self.excel.Visible = settings.VISIBLE
        self.excel.DisplayAlerts = settings.DISPLAYALERTS
        self.file_path = settings.FILES_PATH

    def refresh_save(self, filename):
        filename_path = os.path.join(self.file_path, filename)

        try:
            wb = self.excel.Workbooks.Open(filename_path)
            logger.debug('Create workbook object.')
        except Exception as exc:
            logger.error(exc)
            print('ワークブックオブジェクトの作成に失敗しました。')

        print(f'{filename}の外部接続を更新しています。')
        wb.RefreshAll()
        logger.debug('Refreshed')
        time.sleep(settings.REFRESH_WAIT_TIME)
        print('ファイルを保存しています。')
        wb.Save()
        logger.debug('Save')
        time.sleep(settings.SAVE_WAIT_TIME)
        wb.Close()

    def quit(self):
        self.excel.Quit()
        logger.debug('Quit workbook object')

excel = Excel()
