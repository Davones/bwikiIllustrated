
import os
import logging
from typing import List

from conf.config import AppConfig
from Illustrateds import BaseIllustrated

# 日志句柄
logger = logging.getLogger()


def TreeIllustratedDir(currentPath, IllustratedClass, IllustratedList: List[BaseIllustrated], attributeList: list = []):
    if AppConfig.FileMatchBlackList(currentPath):
        logger.info(f'Path "{currentPath}" will be ignore for Black List Matched')
        return

    if os.path.isdir(currentPath):
        # path
        attributeList.append(currentPath.split('/')[-1])
        logger.debug(f'subpath found {currentPath} of attributeList: {attributeList}')
        for subPath in os.listdir(currentPath):
            TreeIllustratedDir(currentPath=os.path.join(currentPath, subPath), IllustratedClass=IllustratedClass, IllustratedList=IllustratedList, attributeList=attributeList.copy())

    elif os.path.isfile(currentPath):
        # file
        logger.debug(f'file found {currentPath} of attributeList: {attributeList}')
        illustrated = IllustratedClass(filePathAbs=currentPath, attributeList=attributeList.copy())
        IllustratedList.append(illustrated)

    else:
        raise Exception(f'Unknown path for {currentPath}')

    return
