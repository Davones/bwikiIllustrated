
import os
import logging
import time

import pandas as pd

from functions import TreeIllustratedDir
from concurrent.futures import ThreadPoolExecutor
from conf.config import utils_config_init, AppConfig
from Illustrateds import BaseIllustrated, EquipmentIllustrated, SpellIllustrated, MinionIllustrated

from python_library.utils.logUtils import LogUtils


# 配置初始化
utils_config_init()
# 日志句柄
logger = logging.getLogger()
# LogUtils
LogUtils.init_log(log_name='bwiki_illustrated_book-01-CardInfoStandardize', console_log='INFO')


def DoPicOcr(illustratedClass: BaseIllustrated):
    illustratedRootPathAbs = AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.RAW_ROOT_PATH_RE)

    IllustratedList = []
    TreeIllustratedDir(currentPath=illustratedRootPathAbs, IllustratedClass=illustratedClass, IllustratedList=IllustratedList)

    # OCR 识别装备图片
    # IllustratedList = IllustratedList[:3]
    with ThreadPoolExecutor(max_workers=AppConfig.OCR_MAX_WORKERS) as executor:
        taskList = [executor.submit(Illustrated.IllustratedOcr) for Illustrated in IllustratedList]
        while True:
            taskDoneCnt = [task.done() for task in taskList].count(True)
            logger.info(f'{illustratedClass} OCR ing... [{taskDoneCnt}] / [{len(taskList)}]')
            time.sleep(AppConfig.OCR_MONITOR_INTERVAL)
            if taskDoneCnt == len(taskList): break

    # attribute填充
    for Illustrated in IllustratedList:
        Illustrated.FillAttributeList()

    data = pd.DataFrame([illustrated.__dict__ for illustrated in IllustratedList])
    data = data[['Name', 'Description', 'Category', 'AttributeList', 'FilePathAbs', 'OcrResult']]
    print(data)
    dataFile = AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.OCR_XLSX_FILE_PATH)
    datafolder = os.path.split(dataFile)[0]
    if not os.path.exists(datafolder): os.makedirs(datafolder)
    data.to_excel(dataFile)
    logger.info(f'01-DoPicOcr Done [{illustratedClass}] resPath: [{dataFile}]')


if __name__ == '__main__':

    # Deal Equipment pic
    DoPicOcr(illustratedClass=EquipmentIllustrated)

    # Deal Spell pic
    DoPicOcr(illustratedClass=SpellIllustrated)

    # Deal Minion pic
    DoPicOcr(illustratedClass=MinionIllustrated)