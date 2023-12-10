
from typing import List, Tuple

from OcrRepair import ReplaceRepair, RemixReplaceRepair



class BasePicConf:

    RAW_ROOT_PATH_RE = './镜中对决/XXX'
    OCR_XLSX_FILE_PATH = './result/01-ocr_result/XXX.xlsx'
    STD_XLSX_FILE_PATH = './result/02-merge_result/XXX.xlsx'

    MXN_ROOT_PATH_RE = './镜中对决mxn/镜中对决/XX/'
    MXN_MANUAL_DATA_FILE = './镜中对决mxn/镜中对决/XX/XX数据.xlsx'

    STD_DATA_COLUMNS = ['Name', 'Description', 'Category', 'AttributeList', 'FilePathAbs']

    PIC_LAYOUT_CONF = {
        'Name': ((0, 1), (0, 0.2)),
        'Description': ((0, 1), (0.65, 0.9)),
        'Category': ((0.2, 0.8), (0.9, 1)),
    }
    ATTRIBUTE_KEY_WORDS = {'成长', '嘲讽', '击杀', '护盾', '增伤', '疯狂', '遗言', '附着', '先手'}

    BWIKI_FILTER_CONF = {
        '版本': {
            'mece': True,
            'attrSet': {'镜中对决', },
        },
        '星级': {
            'mece': True,
            'attrSet': {'1星', '2星', '3星', '4星', '5星', '6星', },
        },
    }

    @classmethod
    def AnalysLayout(cls, box: List[List[int]], picSize: Tuple[int]):
        horizonList, verticalList = [], []
        for coordinate in box:
            horizonList.append(coordinate[0])
            verticalList.append(coordinate[1])

        for layoutKey in cls.PIC_LAYOUT_CONF:
            horizonBound = cls.PIC_LAYOUT_CONF[layoutKey][0]
            verticalBound = cls.PIC_LAYOUT_CONF[layoutKey][1]
            horizonDisMatchCnt = [horizonBound[0] <= 1.0 * horizon / picSize[0] <= horizonBound[1] for horizon in horizonList].count(False)
            verticalDisMatchCnt = [verticalBound[0] <= 1.0 * vertical / picSize[1] <= verticalBound[1] for vertical in verticalList].count(False)

            if horizonDisMatchCnt == verticalDisMatchCnt == 0:
                return layoutKey

        return None

    @classmethod
    def FilterOfAttributeList(cls, text : str):
        attributeList = []
        for attribute in cls.ATTRIBUTE_KEY_WORDS:
            if attribute in text: attributeList.append(attribute)
        return attributeList



class EquipmentPicConf(BasePicConf):
    RAW_ROOT_PATH_RE = './镜中对决/装备'
    OCR_XLSX_FILE_PATH = './result/01-ocr_result/EquipmentOcrData.xlsx'
    STD_XLSX_FILE_PATH = './result/02-merge_result/EquipmentStdData.xlsx'
    BWIKI_CODE_FILE_PSTH = './result/03-merge_result/EquipmentBwikiCode.txt'
    BWIKI_FILE_FOLDER = './result/03-merge_result/EquipmentPicStd'

    MXN_ROOT_PATH_RE = './镜中对决mxn/镜中对决/装备'

    EXTEND_FIELD = [
        {
            'key': 'bwikiFileName',
            'evalCode': r"""f'''月圆之夜 {illustrated['版本']} {illustrated['类别']} {illustrated['星级'][0]}{illustrated['Name']}.png'''"""
        }
    ]
    BWIKI_FILTER_CONF = [
        {
            'name': '版本',
            'mece': True,
            'show': True,
            'attrSet': {'镜中对决', },
        },
        {
            'name': '类别',
            'mece': True,
            'show': False,
            'attrSet': {'装备', },
        },
        {
            'name': '星级',
            'mece': True,
            'show': True,
            'attrSet': {'1星', '2星', '3星', '4星', '5星', '6星', },
        },
        {
            'name': '特殊',
            'mece': False,
            'show': True,
            'attrSet': {'成长', '嘲讽', '击杀', '护盾', '增伤', '疯狂', '遗言', '附着', '先手', },
        },
    ]
    BWIKI_COLUMNS_CONF = [
        {
            'name': '图标',
            'ifRefCode': True,
            'code': r"""f'''|[[文件:{illustrated['bwikiFileName']}|150px|center|link=]]\n'''""",
        },
        {
            'name': '装备名',
            'ifRefCode': False,
            'valueKey': 'Name',
        },
        {
            'name': '星级',
            'ifRefCode': False,
            'valueKey': '星级',
        },
        {
            'name': '描述',
            'ifRefCode': False,
            'valueKey': 'Description',
        },
    ]

    OCR_REPAIR_CONF = [
        ReplaceRepair(fieldName='Description', oldSubstr='。', newSubstr='，'),
        ReplaceRepair(fieldName='Name', oldSubstr=' ', newSubstr=''),
        ReplaceRepair(fieldName='Name', oldSubstr='芝', newSubstr='之'),
        ReplaceRepair(fieldName='Name', oldSubstr='炅', newSubstr='灵'),
        ReplaceRepair(fieldName='Name', oldSubstr='刃刃', newSubstr='刀刃'),
        ReplaceRepair(fieldName='Name', oldSubstr='矢使', newSubstr='天使'),
        ReplaceRepair(fieldName='Name', oldSubstr='符艾', newSubstr='符文'),
        ReplaceRepair(fieldName='Name', oldSubstr='褰冰', newSubstr='寒冰'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/4星/26-8.png', patternField='FilePathAbs', fieldName='Name', newStr='盾墙'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/4星/25-6.png', patternField='FilePathAbs', fieldName='Name', newStr='重斧'),
        RemixReplaceRepair(pattern='攻击+20该随从攻击后攻击-10', patternField='FilePathAbs', fieldName='Name', newStr='重斧'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/4星/25-3.png', patternField='FilePathAbs', fieldName='Name', newStr='朴素法袍'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/3星/25-8.png', patternField='FilePathAbs', fieldName='Name', newStr='扫帚'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/3星/24-6.png', patternField='FilePathAbs', fieldName='Name', newStr='火苗'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/2星/24-8.png', patternField='FilePathAbs', fieldName='Name', newStr='短剑'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/2星/24-7.png', patternField='FilePathAbs', fieldName='Name', newStr='圆盾'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/28-1.png', patternField='FilePathAbs', fieldName='Name', newStr='磁铁'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/28-6.png', patternField='FilePathAbs', fieldName='Name', newStr='弹弓'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/29-2.png', patternField='FilePathAbs', fieldName='Name', newStr='他者之盾'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/29-6.png', patternField='FilePathAbs', fieldName='Name', newStr='自然印记'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/29-7.png', patternField='FilePathAbs', fieldName='Name', newStr='尖刺羽毛'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/29-4.png', patternField='FilePathAbs', fieldName='Name', newStr='袖箭'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/29-8.png', patternField='FilePathAbs', fieldName='Name', newStr='长弓'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/28-9.png', patternField='FilePathAbs', fieldName='Name', newStr='雷刃'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/6星/32-3.png', patternField='FilePathAbs', fieldName='Name', newStr='鹿角'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/6星/30-1.png', patternField='FilePathAbs', fieldName='Name', newStr='亡灵饼干'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/6星/30-3.png', patternField='FilePathAbs', fieldName='Name', newStr='满月'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/6星/32-5.png', patternField='FilePathAbs', fieldName='Name', newStr='飞斧'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/6星/30-4.png', patternField='FilePathAbs', fieldName='Name', newStr='怀表'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/6星/31-9.png', patternField='FilePathAbs', fieldName='Name', newStr='元素手镯'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/5星/29-2.png', patternField='FilePathAbs', fieldName='Name', newStr='亡者之盾'),
        RemixReplaceRepair(pattern='.*?/镜中对决/装备/4星/25-9.png', patternField='FilePathAbs', fieldName='Name', newStr='巨大化'),
    ]


class SpellPicConf(BasePicConf):
    RAW_ROOT_PATH_RE = './镜中对决/咒术'
    OCR_XLSX_FILE_PATH = './result/01-ocr_result/SpellOcrData.xlsx'
    STD_XLSX_FILE_PATH = './result/02-merge_result/SpellStdData.xlsx'
    BWIKI_CODE_FILE_PSTH = './result/03-merge_result/SpellBwikiCode.txt'
    BWIKI_FILE_FOLDER = './result/03-merge_result/SpellPicStd'

    MXN_ROOT_PATH_RE = './镜中对决mxn/镜中对决/咒术'
    MXN_MANUAL_DATA_FILE = './镜中对决mxn/镜中对决/咒术/咒术数据.xlsx'


    EXTEND_FIELD = [
        {
            'key': 'bwikiFileName',
            'evalCode': r"""f'''月圆之夜 {illustrated['版本']} {illustrated['类别']} {illustrated['星级'][0]}{illustrated['Name']}0.png'''"""
        }
    ]
    BWIKI_FILTER_CONF = [
        {
            'name': '版本',
            'mece': True,
            'show': True,
            'attrSet': {'镜中对决', },
        },
        {
            'name': '类别',
            'mece': True,
            'show': False,
            'attrSet': {'咒术', },
        },
        {
            'name': '星级',
            'mece': True,
            'show': True,
            'attrSet': {'1星', '2星', '3星', '4星', '5星', '6星', },
        },
        {
            'name': '特殊',
            'mece': False,
            'show': True,
            'attrSet': {'成长', '嘲讽', '击杀', '护盾', '增伤', '疯狂', '遗言', '附着', '先手', },
        },
    ]
    BWIKI_COLUMNS_CONF = [
        {
            'name': '图标',
            'ifRefCode': True,
            'code': r"""f'''|[[文件:{illustrated['bwikiFileName']}|150px|center|link=]]\n'''""",
        },
        {
            'name': '装备名',
            'ifRefCode': False,
            'valueKey': 'Name',
        },
        {
            'name': '星级',
            'ifRefCode': False,
            'valueKey': '星级',
        },
        {
            'name': '描述',
            'ifRefCode': False,
            'valueKey': 'Description',
        },
    ]


    OCR_REPAIR_CONF = [
        ReplaceRepair(fieldName='Name', oldSubstr=' ', newSubstr=''),
        ReplaceRepair(fieldName='Name', oldSubstr='[', newSubstr='('),
        ReplaceRepair(fieldName='Name', oldSubstr=']', newSubstr=')'),
        ReplaceRepair(fieldName='Name', oldSubstr='《', newSubstr='('),
        ReplaceRepair(fieldName='Name', oldSubstr='》', newSubstr=')'),
        ReplaceRepair(fieldName='Name', oldSubstr='『', newSubstr='('),
        ReplaceRepair(fieldName='Name', oldSubstr='』', newSubstr=')'),
        ReplaceRepair(fieldName='Name', oldSubstr='女壬', newSubstr='女王'),
        ReplaceRepair(fieldName='Name', oldSubstr='夭平', newSubstr='天平'),
        ReplaceRepair(fieldName='Name', oldSubstr='三头大臂', newSubstr='三头六臂'),
        ReplaceRepair(fieldName='Name', oldSubstr='鼢像', newSubstr='雕像'),
        ReplaceRepair(fieldName='Name', oldSubstr='异娈之力', newSubstr='异变之力'),
        ReplaceRepair(fieldName='Name', oldSubstr='理贮能手', newSubstr='理财能手'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/5星/39-6.png', patternField='FilePathAbs', fieldName='Name', newStr='巧夺'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/6星/42-3.png', patternField='FilePathAbs', fieldName='Name', newStr='血瓶'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/6星/43-5.png', patternField='FilePathAbs', fieldName='Name', newStr='鬼牌'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/4星/36-4.png', patternField='FilePathAbs', fieldName='Name', newStr='理财能手(4)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/4星/36-5.png', patternField='FilePathAbs', fieldName='Name', newStr='剑术训练(4)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/5星/40-7.png', patternField='FilePathAbs', fieldName='Name', newStr='护甲师(5)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/5星/42-4.png', patternField='FilePathAbs', fieldName='Name', newStr='发财(5)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/5星/40-4.png', patternField='FilePathAbs', fieldName='Name', newStr='加速(5)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/5星/39-7.png', patternField='FilePathAbs', fieldName='Name', newStr='精挑细选(5)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/4星/35-9.png', patternField='FilePathAbs', fieldName='Name', newStr='加速(4)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/3星/35-5.png', patternField='FilePathAbs', fieldName='Name', newStr='剑术训练(3)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/3星/34-9.png', patternField='FilePathAbs', fieldName='Name', newStr='抓钩'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/2星/33-5.png', patternField='FilePathAbs', fieldName='Name', newStr='生命庇护(2)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/2星/33-4.png', patternField='FilePathAbs', fieldName='Name', newStr='头脑风暴(2)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/5星/39-9.png', patternField='FilePathAbs', fieldName='Name', newStr='量产工厂(5)'),
        RemixReplaceRepair(pattern='.*?./镜中对决/咒术/5星/41-6.png', patternField='FilePathAbs', fieldName='Name', newStr='饱食(5)'),

    ]


class MinionPicConf(BasePicConf):
    RAW_ROOT_PATH_RE = './镜中对决/金色'
    OCR_XLSX_FILE_PATH = './result/01-ocr_result/MinionGoldenOcrData.xlsx'
    STD_XLSX_FILE_PATH = './result/02-merge_result/MinionStdData.xlsx'
    BWIKI_CODE_FILE_PSTH = './result/03-merge_result/MinionBwikiCode.txt'
    BWIKI_FILE_FOLDER = './result/03-merge_result/MinionPicStd'

    MXN_ROOT_PATH_RE = './镜中对决mxn/镜中对决/随从'
    MXN_MANUAL_DATA_FILE = './镜中对决mxn/镜中对决/随从/随从卡牌数据.xlsx'

    STD_DATA_COLUMNS = ['Name', 'Description', 'Category', 'Attack', 'Health', 'Star', 'AttributeList', 'FilePathAbs']


    EXTEND_FIELD = [
        {
            'key': 'bwikiFileName',
            'evalCode': r"""f'''月圆之夜 {illustrated['版本']} {illustrated['类别']} {illustrated['种族']} {illustrated['星级'][0]}{illustrated['Name']}{1 if illustrated['三连']=='金色' else 0}.png'''"""
        }
    ]
    BWIKI_FILTER_CONF = [
        {
            'name': '版本',
            'mece': True,
            'show': True,
            'attrSet': {'镜中对决', },
        },
        {
            'name': '类别',
            'mece': True,
            'show': False,
            'attrSet': {'随从', },
        },
        {
            'name': '三连',
            'mece': True,
            'show': True,
            'attrSet': {'金色', '普通'},
        },
        {
            'name': '星级',
            'mece': True,
            'show': True,
            'attrSet': {'1星', '2星', '3星', '4星', '5星', '6星', },
        },
        {
            'name': '种族',
            'mece': True,
            'show': True,
            'attrSet': {'战士', '野兽', '幽灵', '龙', '中立', '机械', '自然'},
        },
        {
            'name': '特殊',
            'mece': False,
            'show': True,
            'attrSet': {'成长', '嘲讽', '击杀', '护盾', '增伤', '疯狂', '遗言', '附着', '先手', },
        },
    ]
    BWIKI_COLUMNS_CONF = [
        {
            'name': '图标',
            'ifRefCode': True,
            'code': r"""f'''|[[文件:{illustrated['bwikiFileName']}|150px|center|link=]]\n'''""",
        },
        {
            'name': '装备名',
            'ifRefCode': False,
            'valueKey': 'Name',
        },
        {
            'name': '星级',
            'ifRefCode': False,
            'valueKey': '星级',
        },
        {
            'name': '种族',
            'ifRefCode': False,
            'valueKey': '种族',
        },
        {
            'name': '三连',
            'ifRefCode': False,
            'valueKey': '三连',
        },
        {
            'name': '描述',
            'ifRefCode': False,
            'valueKey': 'Description',
        },
    ]



    OCR_REPAIR_CONF = [
        ReplaceRepair(fieldName='Name', oldSubstr='致瑰', newSubstr='玫瑰'),
        ReplaceRepair(fieldName='Name', oldSubstr='它魂', newSubstr='亡魂'),
        ReplaceRepair(fieldName='Name', oldSubstr='邑型', newSubstr='巨型'),
        ReplaceRepair(fieldName='Name', oldSubstr='自骨', newSubstr='白骨'),
        ReplaceRepair(fieldName='Name', oldSubstr='骑出', newSubstr='骑士'),
        ReplaceRepair(fieldName='Name', oldSubstr='室箱', newSubstr='宝箱'),
        ReplaceRepair(fieldName='Name', oldSubstr='精萸', newSubstr='精英'),
        ReplaceRepair(fieldName='Name', oldSubstr='首颔', newSubstr='首领'),
        ReplaceRepair(fieldName='Category', oldSubstr='战鼢', newSubstr='战士'),
        ReplaceRepair(fieldName='Category', oldSubstr='机鼢', newSubstr='机械'),
        ReplaceRepair(fieldName='Category', oldSubstr='鼢鼢', newSubstr='幽灵'),
        ReplaceRepair(fieldName='Category', oldSubstr='泷', newSubstr='龙'),
        ReplaceRepair(fieldName='Category', oldSubstr='求', newSubstr='龙'),
        ReplaceRepair(fieldName='Category', oldSubstr='鼢', newSubstr='龙'),


        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4552x3060_2023-11-27_17-11-04.png', patternField='FilePathAbs', fieldName='Name', newStr='窃贼'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4552x3060_2023-11-27_17-12-44.png', patternField='FilePathAbs', fieldName='Name', newStr='法力图腾'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4552x3060_2023-11-27_17-13-49.png', patternField='FilePathAbs', fieldName='Name', newStr='酩酊酒客'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4552x3060_2023-11-27_17-14-08.png', patternField='FilePathAbs', fieldName='Name', newStr='废土旅人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4552x3060_2023-11-27_17-15-17.png', patternField='FilePathAbs', fieldName='Name', newStr='杀手鱼人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-33-27.png', patternField='FilePathAbs', fieldName='Name', newStr='勇敢挑战者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-33-46.png', patternField='FilePathAbs', fieldName='Name', newStr='魔女'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-36-40.png', patternField='FilePathAbs', fieldName='Name', newStr='守卫'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-47-48.png', patternField='FilePathAbs', fieldName='Name', newStr='宫廷管家'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-48-02.png', patternField='FilePathAbs', fieldName='Name', newStr='贴身保镖'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-48-20.png', patternField='FilePathAbs', fieldName='Name', newStr='老猎人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-48-31.png', patternField='FilePathAbs', fieldName='Name', newStr='巡逻兵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-48-41.png', patternField='FilePathAbs', fieldName='Name', newStr='丛林巨人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-48-59.png', patternField='FilePathAbs', fieldName='Name', newStr='玫瑰盾卫'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-49-10.png', patternField='FilePathAbs', fieldName='Name', newStr='神秘铁匠'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-49-21.png', patternField='FilePathAbs', fieldName='Name', newStr='双持盾兵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-49-37.png', patternField='FilePathAbs', fieldName='Name', newStr='蔷薇骑士'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-49-46.png', patternField='FilePathAbs', fieldName='Name', newStr='纵火者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-49-55.png', patternField='FilePathAbs', fieldName='Name', newStr='裁决者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-50-04.png', patternField='FilePathAbs', fieldName='Name', newStr='野牛骑士长'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-50-14.png', patternField='FilePathAbs', fieldName='Name', newStr='受祝福的勇士'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-50-25.png', patternField='FilePathAbs', fieldName='Name', newStr='骑士铠甲'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-50-35.png', patternField='FilePathAbs', fieldName='Name', newStr='持盾战士'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-51-03.png', patternField='FilePathAbs', fieldName='Name', newStr='小狼狗'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-51-12.png', patternField='FilePathAbs', fieldName='Name', newStr='鹳鸟'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-51-21.png', patternField='FilePathAbs', fieldName='Name', newStr='蝴蝶看守'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-51-32.png', patternField='FilePathAbs', fieldName='Name', newStr='信鸽'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-51-40.png', patternField='FilePathAbs', fieldName='Name', newStr='蹦蹦鹿'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-51-47.png', patternField='FilePathAbs', fieldName='Name', newStr='萤火虫'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-51-56.png', patternField='FilePathAbs', fieldName='Name', newStr='小蜜蜂'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-52-11.png', patternField='FilePathAbs', fieldName='Name', newStr='袖珍枪手'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-52-21.png', patternField='FilePathAbs', fieldName='Name', newStr='猎豹'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-52-40.png', patternField='FilePathAbs', fieldName='Name', newStr='黑马'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-53-20.png', patternField='FilePathAbs', fieldName='Name', newStr='炙火蝎'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-53-30.png', patternField='FilePathAbs', fieldName='Name', newStr='地狱三头犬'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-53-39.png', patternField='FilePathAbs', fieldName='Name', newStr='丛林枭兽'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-53-52.png', patternField='FilePathAbs', fieldName='Name', newStr='穿山甲弟弟'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-54-00.png', patternField='FilePathAbs', fieldName='Name', newStr='怒熊'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-54-08.png', patternField='FilePathAbs', fieldName='Name', newStr='猫头鹰法师'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-54-27.png', patternField='FilePathAbs', fieldName='Name', newStr='毒蛇女王'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-54-38.png', patternField='FilePathAbs', fieldName='Name', newStr='金刚'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-54-46.png', patternField='FilePathAbs', fieldName='Name', newStr='鼠王'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-54-55.png', patternField='FilePathAbs', fieldName='Name', newStr='绿毛哥'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-55-03.png', patternField='FilePathAbs', fieldName='Name', newStr='野猪'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-55-15.png', patternField='FilePathAbs', fieldName='Name', newStr='火枪支配者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-55-32.png', patternField='FilePathAbs', fieldName='Name', newStr='机械熊仔'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-55-40.png', patternField='FilePathAbs', fieldName='Name', newStr='防御炮台'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_17-55-48.png', patternField='FilePathAbs', fieldName='Name', newStr='钻头'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-03-10.png', patternField='FilePathAbs', fieldName='Name', newStr='全副武装'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-03-22.png', patternField='FilePathAbs', fieldName='Name', newStr='改装师'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-03-30.png', patternField='FilePathAbs', fieldName='Name', newStr='机械兔'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-03-41.png', patternField='FilePathAbs', fieldName='Name', newStr='充能炮'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-03-55.png', patternField='FilePathAbs', fieldName='Name', newStr='机械信使'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-04-09.png', patternField='FilePathAbs', fieldName='Name', newStr='零件商贩'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-04-17.png', patternField='FilePathAbs', fieldName='Name', newStr='防御要塞'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-04-25.png', patternField='FilePathAbs', fieldName='Name', newStr='扳手助理'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-04-44.png', patternField='FilePathAbs', fieldName='Name', newStr='智能机器人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-04-55.png', patternField='FilePathAbs', fieldName='Name', newStr='机械犬'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-05-03.png', patternField='FilePathAbs', fieldName='Name', newStr='玩具商人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-05-10.png', patternField='FilePathAbs', fieldName='Name', newStr='拾荒者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-05-16.png', patternField='FilePathAbs', fieldName='Name', newStr='制造能手'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-05-26.png', patternField='FilePathAbs', fieldName='Name', newStr='钢筋铁甲'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-05-33.png', patternField='FilePathAbs', fieldName='Name', newStr='发条淑女'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-05-43.png', patternField='FilePathAbs', fieldName='Name', newStr='铁皮人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-05-54.png', patternField='FilePathAbs', fieldName='Name', newStr='扩音器'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-06-12.png', patternField='FilePathAbs', fieldName='Name', newStr='钢铁之躯'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-06-20.png', patternField='FilePathAbs', fieldName='Name', newStr='机械套娃'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-06-29.png', patternField='FilePathAbs', fieldName='Name', newStr='小树精'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-06-36.png', patternField='FilePathAbs', fieldName='Name', newStr='魔法树苗'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-06-46.png', patternField='FilePathAbs', fieldName='Name', newStr='南瓜斥候'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-06-52.png', patternField='FilePathAbs', fieldName='Name', newStr='小石精'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-07-00.png', patternField='FilePathAbs', fieldName='Name', newStr='食人花'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-07-07.png', patternField='FilePathAbs', fieldName='Name', newStr='南瓜卫士'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-07-15.png', patternField='FilePathAbs', fieldName='Name', newStr='草灵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-07-25.png', patternField='FilePathAbs', fieldName='Name', newStr='古树'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-07-39.png', patternField='FilePathAbs', fieldName='Name', newStr='恐怖番茄'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-07-45.png', patternField='FilePathAbs', fieldName='Name', newStr='魔法南瓜'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-07-56.png', patternField='FilePathAbs', fieldName='Name', newStr='石精灵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-08-05.png', patternField='FilePathAbs', fieldName='Name', newStr='小蘑菇'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-08-14.png', patternField='FilePathAbs', fieldName='Name', newStr='林地看守'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-08-24.png', patternField='FilePathAbs', fieldName='Name', newStr='狂乱树精'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-08-31.png', patternField='FilePathAbs', fieldName='Name', newStr='智慧石精'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-08-49.png', patternField='FilePathAbs', fieldName='Name', newStr='自然仙灵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-08-57.png', patternField='FilePathAbs', fieldName='Name', newStr='苔藓骑士'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-09-06.png', patternField='FilePathAbs', fieldName='Name', newStr='黑玫瑰'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-09-13.png', patternField='FilePathAbs', fieldName='Name', newStr='蘑菇长老'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-09-22.png', patternField='FilePathAbs', fieldName='Name', newStr='孢子小姐'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-09-32.png', patternField='FilePathAbs', fieldName='Name', newStr='孢子女巫'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-09-42.png', patternField='FilePathAbs', fieldName='Name', newStr='花匠'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-09-50.png', patternField='FilePathAbs', fieldName='Name', newStr='石精巨兽'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-10-11.png', patternField='FilePathAbs', fieldName='Name', newStr='梦境之树'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-10-19.png', patternField='FilePathAbs', fieldName='Name', newStr='蘑菇国王'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-10-34.png', patternField='FilePathAbs', fieldName='Name', newStr='鬼火'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-10-43.png', patternField='FilePathAbs', fieldName='Name', newStr='亡魂宝箱'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-11-00.png', patternField='FilePathAbs', fieldName='Name', newStr='罗生门'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-11-18.png', patternField='FilePathAbs', fieldName='Name', newStr='夺魂者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-11-31.png', patternField='FilePathAbs', fieldName='Name', newStr='亡魂吹笛者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-11-46.png', patternField='FilePathAbs', fieldName='Name', newStr='灵魂鼓手'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-11-53.png', patternField='FilePathAbs', fieldName='Name', newStr='处刑人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-12-07.png', patternField='FilePathAbs', fieldName='Name', newStr='引路者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-12-16.png', patternField='FilePathAbs', fieldName='Name', newStr='幽灵大盗'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-12-25.png', patternField='FilePathAbs', fieldName='Name', newStr='幽灵船长'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-12-36.png', patternField='FilePathAbs', fieldName='Name', newStr='亡魂宝匣'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-12-52.png', patternField='FilePathAbs', fieldName='Name', newStr='亡魂铁匠'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-13-01.png', patternField='FilePathAbs', fieldName='Name', newStr='亡魂执政官'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-13-10.png', patternField='FilePathAbs', fieldName='Name', newStr='魂引者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-13-42.png', patternField='FilePathAbs', fieldName='Name', newStr='灵魂祭司'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-17-38.png', patternField='FilePathAbs', fieldName='Name', newStr='懊悔者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-17-58.png', patternField='FilePathAbs', fieldName='Name', newStr='侍僧'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-18-06.png', patternField='FilePathAbs', fieldName='Name', newStr='亡魂音乐盒'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-18-16.png', patternField='FilePathAbs', fieldName='Name', newStr='石中剑'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-18-26.png', patternField='FilePathAbs', fieldName='Name', newStr='灾厄'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-18-34.png', patternField='FilePathAbs', fieldName='Name', newStr='灵魂共鸣者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-18-50.png', patternField='FilePathAbs', fieldName='Name', newStr='古堡幽灵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-19-24.png', patternField='FilePathAbs', fieldName='Name', newStr='烈焰雏龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-19-33.png', patternField='FilePathAbs', fieldName='Name', newStr='保护之龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-19-39.png', patternField='FilePathAbs', fieldName='Name', newStr='超凡驯龙师'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-19-55.png', patternField='FilePathAbs', fieldName='Name', newStr='大地之龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-20-02.png', patternField='FilePathAbs', fieldName='Name', newStr='炎翼龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-20-10.png', patternField='FilePathAbs', fieldName='Name', newStr='法术龙灵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-20-16.png', patternField='FilePathAbs', fieldName='Name', newStr='龙蛋吞噬者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-20-30.png', patternField='FilePathAbs', fieldName='Name', newStr='死亡之龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-20-38.png', patternField='FilePathAbs', fieldName='Name', newStr='风龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-20-53.png', patternField='FilePathAbs', fieldName='Name', newStr='水之龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-21-00.png', patternField='FilePathAbs', fieldName='Name', newStr='幽龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-21-21.png', patternField='FilePathAbs', fieldName='Name', newStr='守护之龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-21-36.png', patternField='FilePathAbs', fieldName='Name', newStr='噬魂之龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-21-43.png', patternField='FilePathAbs', fieldName='Name', newStr='圣龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-21-49.png', patternField='FilePathAbs', fieldName='Name', newStr='灾厄巨龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-21-57.png', patternField='FilePathAbs', fieldName='Name', newStr='强袭飞龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-22-07.png', patternField='FilePathAbs', fieldName='Name', newStr='雌火龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-22-18.png', patternField='FilePathAbs', fieldName='Name', newStr='栖湖古龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-22-25.png', patternField='FilePathAbs', fieldName='Name', newStr='白骨龙灵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-22-33.png', patternField='FilePathAbs', fieldName='Name', newStr='龙骑士队长'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-23-04.png', patternField='FilePathAbs', fieldName='Name', newStr='大厨'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4920x3060_2023-11-27_18-23-20.png', patternField='FilePathAbs', fieldName='Name', newStr='变色龙'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-33-27.png', patternField='FilePathAbs', fieldName='Name', newStr='盾弩手'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-33-49.png', patternField='FilePathAbs', fieldName='Name', newStr='刽子手'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-34-01.png', patternField='FilePathAbs', fieldName='Name', newStr='队长'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-34-44.png', patternField='FilePathAbs', fieldName='Name', newStr='小鬼娃娃'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-35-26.png', patternField='FilePathAbs', fieldName='Name', newStr='神射手'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-35-36.png', patternField='FilePathAbs', fieldName='Name', newStr='武器小偷'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-35-48.png', patternField='FilePathAbs', fieldName='Name', newStr='催眠师'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-35-56.png', patternField='FilePathAbs', fieldName='Name', newStr='石像鬼'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-36-05.png', patternField='FilePathAbs', fieldName='Name', newStr='集结号手'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-36-16.png', patternField='FilePathAbs', fieldName='Name', newStr='探险者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-36-24.png', patternField='FilePathAbs', fieldName='Name', newStr='魔靴'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-37-24.png', patternField='FilePathAbs', fieldName='Name', newStr='寻宝狗头人'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-37-40.png', patternField='FilePathAbs', fieldName='Name', newStr='魔法精灵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-37-49.png', patternField='FilePathAbs', fieldName='Name', newStr='抄写员'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-38-16.png', patternField='FilePathAbs', fieldName='Name', newStr='防御者'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-38-31.png', patternField='FilePathAbs', fieldName='Name', newStr='鬼娃娃'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-38-49.png', patternField='FilePathAbs', fieldName='Name', newStr='泉水之灵'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-38-58.png', patternField='FilePathAbs', fieldName='Name', newStr='魔镜'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-39-25.png', patternField='FilePathAbs', fieldName='Name', newStr='沉默医师'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-39-32.png', patternField='FilePathAbs', fieldName='Name', newStr='死灵傀儡师'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-39-43.png', patternField='FilePathAbs', fieldName='Name', newStr='渔夫'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-39-52.png', patternField='FilePathAbs', fieldName='Name', newStr='伐木工叔叔'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-40-04.png', patternField='FilePathAbs', fieldName='Name', newStr='逃犯'),
        RemixReplaceRepair(pattern='.*?./镜中对决/金色/screen_4964x3116_2023-11-27_18-40-12.png', patternField='FilePathAbs', fieldName='Name', newStr='见习侍卫'),
    ]
