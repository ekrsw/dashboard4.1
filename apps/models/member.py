import logging
import os
import pandas as pd

import settings

logging.basicConfig(filename=settings.LOG_FILE, level=settings.LOGLEVEL)
logger = logging.getLogger(__name__)

class Member(object):
    def __init__(self):
        member_file = os.path.join(settings.FILES_PATH, settings.MEMBER_LIST)
        
        if os.path.exists(member_file):
            df = pd.read_excel(member_file).fillna('')
            df['グループ'] = df['グループ'].astype(int)
            df.index = df['氏名']
            self.member_df = df
        else:
            logger.error(f"File not found: {member_file}")
            raise FileNotFoundError(f"File not found: {member_file}")
