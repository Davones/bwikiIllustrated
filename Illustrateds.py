
import ast
from collections import Counter
import filecmp
import logging
import os


from PIL import Image
import easyocr
import pandas as pd

from conf.config import AppConfig
from conf.PicConf import BasePicConf, EquipmentPicConf, MinionPicConf, SpellPicConf, HeroPicConf


logger = logging.getLogger()

class BaseIllustrated:
    PIC_CONF = BasePicConf

    def __init__(self, filePathAbs: str = '', attributeList: list = []):
        self.PicConf = self.PIC_CONF
        self.FilePathAbs = filePathAbs
        self.FileNameNoSuffix = os.path.split(self.FilePathAbs)[1].split('.')[0]
        self.AttributeList = attributeList.copy()

        if self.FilePathAbs != '':
            self.ImageSize = Image.open(self.FilePathAbs).size
        self.OcrResult = []

        self.Name = ''
        self.Description = ''
        self.Category = ''

    def IllustratedOcr(self):
        reader = easyocr.Reader(['ch_sim', 'en'])
        self.OcrResult = reader.readtext(self.FilePathAbs)

        for textOcr in self.OcrResult:
            layoutKey = self.PicConf.AnalysLayout(box=textOcr[0], picSize=self.ImageSize)
            ocrText = textOcr[1]
            confidence = textOcr[1]
            if layoutKey is None:
                logger.warning(f'{type(self)} Unknown Layout Text [{ocrText}]-[{confidence}] in pic [{self.FilePathAbs}], box={textOcr[0]}, picSize=[{self.ImageSize}]')
                # raise Exception(f'Unknown layoutKey')
                continue

            if not hasattr(self, layoutKey):
                logger.critical(f'Unknown layoutKey [{layoutKey}]')
                raise Exception(f'Unknown layoutKey')
            # if len(getattr(self, layoutKey)) != 0:
            #     setattr(self, layoutKey, getattr(self, layoutKey) + '\n')
            setattr(self, layoutKey, getattr(self, layoutKey) + ocrText)

        # Ocr结果修正
        for repair in self.PicConf.OCR_REPAIR_CONF:
            repair.DoRepair(self)

        logger.debug(f'IllustratedOcr done of [{self.FilePathAbs}]: {self.__dict__}')

    def FillAttributeList(self):
        self.AttributeList.extend(self.PicConf.FilterOfAttributeList(self.Description))

    def AnalysMxnPicName(self):
        raise NotImplementedError()

    @classmethod
    def DealMxnAndOcrData(cls, mergeData: dict):
        res = {}
        res['Name'] = mergeData['Name']
        res['Category'] = mergeData['Category_mxn'] if len(mergeData['Category_mxn']) != 0 else mergeData['Category_ocr']
        res['Description'] = mergeData['Description_mxn'] if len(mergeData['Description_mxn']) != 0 else mergeData['Description_ocr']
        attributeList = mergeData['AttributeList_mxn']
        attributeList.extend(ast.literal_eval(mergeData['AttributeList_ocr']))
        res['AttributeList'] = list({}.fromkeys(attributeList).keys())
        if len(mergeData['FilePathAbs_mxn']) > 0 and mergeData['FilePathAbs_ocr']:
            if not filecmp.cmp(mergeData['FilePathAbs_mxn'], mergeData['FilePathAbs_ocr']):
                logger.error(f'FilePathAbs_ocr [{mergeData["FilePathAbs_ocr"]}] not equal FilePathAbs_mxn [{mergeData["FilePathAbs_mxn"]}]')
                raise f'FilePathAbs file not equal'
        res['FilePathAbs'] = mergeData['FilePathAbs_mxn'] if len(mergeData['FilePathAbs_mxn']) != 0 else mergeData['FilePathAbs_ocr']
        return res

    @classmethod
    def MxnDataPreprocessing(cls, illustratedList):
        pass


class EquipmentIllustrated(BaseIllustrated):
    PIC_CONF = EquipmentPicConf


    def AnalysMxnPicName(self):
        stdNameSplited = self.FileNameNoSuffix.split('_')
        for attribute in stdNameSplited[:-1]:
            self.AttributeList.append(attribute)
        self.AttributeList.append(f'{stdNameSplited[-1][0]}星')
        self.AttributeList.append(f'{"金色" if stdNameSplited[-1][-1] == "1" else "普通"}')
        self.Name = stdNameSplited[-1][1:]



class SpellIllustrated(BaseIllustrated):
    PIC_CONF = SpellPicConf


    def AnalysMxnPicName(self):
        stdNameSplited = self.FileNameNoSuffix.split('_')
        for attribute in stdNameSplited[:-1]:
            self.AttributeList.append(attribute)
        self.AttributeList.append(f'{stdNameSplited[-1][0]}星')
        self.AttributeList.append(f'{"金色" if stdNameSplited[-1][-1] == "1" else "普通"}')
        self.Name = stdNameSplited[-1][1:-1]

    @classmethod
    def MxnDataPreprocessing(cls, illustratedList):
        super().MxnDataPreprocessing(illustratedList)

        # Name($cost)
        nameCnt = Counter([illustrated.Name for illustrated in illustratedList])
        for illustrated in illustratedList:
            if nameCnt[illustrated.Name] > 1:
                illustrated.Name = f'{illustrated.Name}({illustrated.FileNameNoSuffix.split("_")[-1][0]})'

        # Manual Data
        manualData = pd.read_excel(AppConfig.ToDataAbsPath(cls.PIC_CONF.MXN_MANUAL_DATA_FILE))
        manualData.set_index(['名称'], inplace=True)
        for illustrated in illustratedList:
            illustrated.Description = manualData.loc[illustrated.FileNameNoSuffix]['效果']



class MinionIllustrated(BaseIllustrated):
    PIC_CONF = MinionPicConf

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Category = ''
        self.Attack = 0
        self.Health = 0
        self.Star = 0


    def AnalysMxnPicName(self):
        stdNameSplited = self.FileNameNoSuffix.split('_')
        for attribute in stdNameSplited[:-1]:
            self.AttributeList.append(attribute)
        self.AttributeList.append(f'{stdNameSplited[-1][0]}星')
        self.AttributeList.append(f'{"金色" if stdNameSplited[-1][-1] == "1" else "普通"}')
        self.Name = stdNameSplited[-1][1:-1]
        self.Category = stdNameSplited[-2]


    @classmethod
    def MxnDataPreprocessing(cls, illustratedList):
        super().MxnDataPreprocessing(illustratedList)

        # Manual Data
        manualData = pd.read_excel(AppConfig.ToDataAbsPath(cls.PIC_CONF.MXN_MANUAL_DATA_FILE))
        manualData.set_index(['名称'], inplace=True)
        for illustrated in illustratedList:
            illustrated.Description = manualData.loc[illustrated.Name]['描述']
            illustrated.Star = int(manualData.loc[illustrated.Name]['星级'])
            illustrated.Category = manualData.loc[illustrated.Name]['种族']
            illustrated.Attack = int(manualData.loc[illustrated.Name]['攻击值'])
            illustrated.Health = int(manualData.loc[illustrated.Name]['生命值'])


class HeroIllustrated(BaseIllustrated):
    PIC_CONF = HeroPicConf

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

