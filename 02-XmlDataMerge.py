
import ast
import os
import logging
import time

import pandas as pd

from functions import TreeIllustratedDir
from conf.config import utils_config_init, AppConfig
from conf.PicConf import BasePicConf
from Illustrateds import BaseIllustrated, EquipmentIllustrated, SpellIllustrated, MinionIllustrated


from python_library.utils.logUtils import LogUtils


# 配置初始化
utils_config_init()
# 日志句柄
logger = logging.getLogger()
# LogUtils
LogUtils.init_log(log_name='bwiki_illustrated_book-01-XmlDataMerge', console_log='INFO')


def ReadMxnData(illustratedClass: BaseIllustrated):
    illustratedRootPathAbs = AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.MXN_ROOT_PATH_RE)

    IllustratedList = []
    TreeIllustratedDir(currentPath=illustratedRootPathAbs, IllustratedClass=illustratedClass, IllustratedList=IllustratedList, attributeList=[])
    for illustrated in IllustratedList:
        illustrated.AnalysMxnPicName()

    illustratedClass.MxnDataPreprocessing(IllustratedList)

    return pd.DataFrame([illustrated.__dict__ for illustrated in IllustratedList])


def XmlDataMerge(illustratedClass: BaseIllustrated):
    mxnData = ReadMxnData(illustratedClass=illustratedClass)
    ocrData = pd.read_excel(AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.OCR_XLSX_FILE_PATH))
    # assert mxnData.shape[0] == ocrData.shape[0]

    mxnData = mxnData[illustratedClass.PIC_CONF.STD_DATA_COLUMNS]
    ocrData = ocrData[illustratedClass.PIC_CONF.STD_DATA_COLUMNS]

    # 对称差集为空
    # assert mxnData[~mxnData['Name'].isin(ocrData['Name'])].shape[0] == ocrData[~ocrData['Name'].isin(mxnData['Name'])].shape[0] == 0

    # 合并数据
    xmlDataMerged = pd.merge(left=mxnData, right=ocrData, how='outer', on=['Name'], suffixes=['_mxn', '_ocr'])
    if not mxnData.shape[0] == ocrData.shape[0] == xmlDataMerged.shape[0]:
        logger.error(f'Symmetric Difference set of mxnData and ocrData not empty:\n{mxnData[~mxnData["Name"].isin(ocrData["Name"])]}\n{ocrData[~ocrData["Name"].isin(mxnData["Name"])]}')
        raise Exception('Symmetric Difference set of mxnData and ocrData not empty')

    mergeDataList = []
    for _, row in xmlDataMerged.iterrows():
        mergeDataDict = illustratedClass.DealMxnAndOcrData(row.to_dict())
        mergeDataList.append(mergeDataDict)
    mergeDataList = pd.DataFrame(mergeDataList)

    dataFile = AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.STD_XLSX_FILE_PATH)
    datafolder = os.path.split(dataFile)[0]
    if not os.path.exists(datafolder): os.makedirs(datafolder)
    mergeDataList.to_excel(dataFile)
    logger.info(f'02-XmlDataMerge Done [{illustratedClass}] resPath: [{dataFile}]')


def MinionDataConcat(illustratedClass: BaseIllustrated):
    normalData = ReadMxnData(illustratedClass=illustratedClass)
    goldenData = pd.read_excel(AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.OCR_XLSX_FILE_PATH))
    goldenData['Attack'] = goldenData['Health'] = goldenData['Star'] = 0

    normalData = normalData[illustratedClass.PIC_CONF.STD_DATA_COLUMNS]
    goldenData = goldenData[illustratedClass.PIC_CONF.STD_DATA_COLUMNS]

    # fill golden data
    normalData.set_index(['Name'], inplace=True)
    for index, row in goldenData.iterrows():
        if row['Name'] not in normalData.index: continue
        goldenData.at[index, 'Attack'] = normalData.loc[row['Name']]['Attack'] * 2
        goldenData.at[index, 'Health'] = normalData.loc[row['Name']]['Health'] * 2
        goldenData.at[index, 'Star'] = normalData.loc[row['Name']]['Star']
        goldenData.at[index, 'Category'] = normalData.loc[row['Name']]['Category']
        attributeList = ast.literal_eval(goldenData.at[index, 'AttributeList'])
        attributeList.extend(normalData.loc[row['Name']]['AttributeList'])
        attributeList.remove('金色')
        attributeList.remove('普通')
        attributeList = list(set(attributeList))
        goldenData.at[index, 'AttributeList'] = attributeList.copy()
        normalData.at[row['Name'], 'AttributeList'] = attributeList.copy()
        goldenData.at[index, 'AttributeList'].append('金色')
        normalData.loc[row['Name']]['AttributeList'].append('普通')
    normalData.reset_index(inplace=True)

    # TODO
    goldenData = goldenData[goldenData['Attack'] > 0]


    # concat dataframe
    concatData = pd.concat([normalData, goldenData])
    concatData.sort_values(['Name'], inplace=True)

    dataFile = AppConfig.ToDataAbsPath(illustratedClass.PIC_CONF.STD_XLSX_FILE_PATH)
    datafolder = os.path.split(dataFile)[0]
    if not os.path.exists(datafolder): os.makedirs(datafolder)
    concatData.to_excel(dataFile)
    logger.info(f'02-XmlDataMerge Done [{illustratedClass}] resPath: [{dataFile}]')



if __name__ == '__main__':
    # XmlDataMerge(illustratedClass=EquipmentIllustrated)
    #
    # XmlDataMerge(illustratedClass=SpellIllustrated)
    #
    # MinionDataConcat(illustratedClass=MinionIllustrated)
    pass