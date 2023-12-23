
import ast
import os
import logging
import time
from typing import List

from PIL import Image
import pandas as pd

from functions import TreeIllustratedDir
from conf.config import utils_config_init, AppConfig
from conf.PicConf import BasePicConf
from Illustrateds import BaseIllustrated, EquipmentIllustrated, SpellIllustrated, MinionIllustrated, HeroIllustrated


from python_library.utils.logUtils import LogUtils


# 配置初始化
utils_config_init()
# 日志句柄
logger = logging.getLogger()
# LogUtils
LogUtils.init_log(log_name='bwiki_illustrated_book-01-XmlDataMerge', console_log='INFO')


def ReadStdXmlData(illustratedClass: BaseIllustrated):
    stdIllustratedData = pd.read_excel(AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.VERIFIED_XLSX_FILE_PATH))

    illustratedList = []
    for _, row in stdIllustratedData.iterrows():
        illustrated = row.to_dict()
        illustrated['AttributeList'] = ast.literal_eval(illustrated['AttributeList'])
        for filterConf in illustratedClass.PIC_CONF.BWIKI_FILTER_CONF:
            if filterConf['name'] in illustrated: continue
            illustrated[filterConf['name']] = None if filterConf['mece'] else []
            for attr in illustrated['AttributeList']:
                if attr in filterConf['attrSet']:
                    if filterConf['mece']: illustrated[filterConf['name']] = attr
                    else: illustrated[filterConf['name']].append(attr)
        for extendFieldConf in illustratedClass.PIC_CONF.EXTEND_FIELD:
            illustrated[extendFieldConf['key']] = eval(extendFieldConf['evalCode'])
        illustratedList.append(illustrated)

    return illustratedList


def ResveBwikiFile(illustratedClass: BaseIllustrated, illustratedList: List[dict]):
    resaveFolder = AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.BWIKI_FILE_FOLDER)
    if not os.path.exists(resaveFolder): os.makedirs(resaveFolder)

    for illustrated in illustratedList:
        image = Image.open(illustrated['FilePathAbs'])
        image.save(os.path.join(resaveFolder, illustrated['bwikiFileName']))


def GenBwikiFilterCode(illustratedClass: BaseIllustrated):
    filterCode = '''{|class="wikitable" style="width:100%"\n|-\n!width="80px"|查看全部\n|\n{{筛选项|0|0|查看全部}}\n'''

    for index, filterConf in enumerate(illustratedClass.PIC_CONF.BWIKI_FILTER_CONF):
        if not filterConf['show']: continue
        filterCode = filterCode + f'''|-\n!{filterConf['name']}\n|\n'''
        for attr in filterConf['attrSet']:
            filterCode = filterCode + f'''{{{{筛选项|{index+1}|{attr}|}}}}\n'''

    filterCode = filterCode + '''|}\n'''
    return filterCode


def GenBwikiIllustratedCode(illustratedClass: BaseIllustrated, illustratedList: List[dict]):
    illustratedCode = '''<div style="overflow-x:scroll;">\n{|id="CardSelectTr" class="CardSelect wikitable sortable"  style="width:100%;text-align:center"\n|-id="CardSelectTabHeader"\n'''

    # 表头
    for columnsConf in illustratedClass.PIC_CONF.BWIKI_COLUMNS_CONF:
        illustratedCode = illustratedCode + f'''!{columnsConf['name']}\n'''

    # 表体
    for illustrated in illustratedList:
        # 筛选项
        illustratedCode = illustratedCode + '''|-class="divsort"'''
        for index, filterConf in enumerate(illustratedClass.PIC_CONF.BWIKI_FILTER_CONF):
            if filterConf['mece']:
                illustratedCode = illustratedCode + f''' data-param{index + 1}="{illustrated[filterConf['name']]}"'''
            else:
                for attr in illustrated[filterConf['name']]: illustratedCode = illustratedCode + f''' data-param{index + 1}="{attr}"'''
        illustratedCode = illustratedCode + '\n'

        # 内容
        for columnsConf in illustratedClass.PIC_CONF.BWIKI_COLUMNS_CONF:
            if columnsConf['ifRefCode']:
                illustratedCode = illustratedCode + eval(columnsConf['code'])
            else:
                illustratedCode = illustratedCode + f'''| {illustrated[columnsConf['valueKey']]}\n'''

    illustratedCode = illustratedCode + '''|}\n</div>\n'''
    return illustratedCode


def GenBwikiCode(illustratedClass: BaseIllustrated, resavePic: bool = False):
    # 读取xml数据
    illustratedList = ReadStdXmlData(illustratedClass=illustratedClass)

    # 重命名bwiki文件名
    if resavePic:
        ResveBwikiFile(illustratedClass=illustratedClass, illustratedList=illustratedList)

    # 生成表头
    filterCode = GenBwikiFilterCode(illustratedClass=illustratedClass)

    # 生成图鉴列表
    illustratedCode = GenBwikiIllustratedCode(illustratedClass=illustratedClass, illustratedList=illustratedList)

    bwikiCode = filterCode + illustratedCode


    dataFile = AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.BWIKI_CODE_FILE_PSTH)
    datafolder = os.path.split(dataFile)[0]
    if not os.path.exists(datafolder): os.makedirs(datafolder)
    with open(dataFile, 'w') as file: file.write(bwikiCode)
    logger.info(f'03-GenBwikiCode Done [{illustratedClass}] resPath: [{dataFile}]')


if __name__ == '__main__':
    GenBwikiCode(illustratedClass=EquipmentIllustrated, resavePic = False)

    GenBwikiCode(illustratedClass=SpellIllustrated, resavePic = False)

    GenBwikiCode(illustratedClass=MinionIllustrated, resavePic = False)

    GenBwikiCode(illustratedClass=HeroIllustrated, resavePic=False)
