
import logging
import os

import pandas as pd

from python_library.utils.baseconfig import BaseConfig


logger = logging.getLogger()


class PandasConfig(BaseConfig):
    PD_DISPLAY_ROWS  = None
    PD_DISPLAY_COLS  = 100
    PD_DISPLAY_WIDTH = 1000


class PandasUtils:

    @staticmethod
    def pandas_config_init():
        pd.set_option('display.max_rows', PandasConfig.PD_DISPLAY_ROWS)
        pd.set_option('display.min_rows', PandasConfig.PD_DISPLAY_ROWS)
        pd.set_option('display.max_columns', PandasConfig.PD_DISPLAY_COLS)
        pd.set_option('display.width', PandasConfig.PD_DISPLAY_WIDTH)
        pd.set_option('display.max_colwidth', PandasConfig.PD_DISPLAY_WIDTH)
        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)
        pd.set_option('expand_frame_repr', False)


    # 更新pandas.DataFrame写入文件
    @staticmethod
    def appendDataFrameToLocalFile(file_name, append_data, folder_abs_path=None, sort_values=[], drop_duplicates=[]):
        folder_abs_path = folder_abs_path if folder_abs_path else PandasConfig.APP_DATA_PATH()
        if not os.path.exists(folder_abs_path): os.mkdir(folder_abs_path)
        filepath = os.path.join(folder_abs_path, file_name)
        logger.debug(f"Start append DataFrame to file [{filepath}]. append_data.shape=[{append_data.shape}], sort_values=[{sort_values}], drop_duplicates=[{drop_duplicates}]...")

        if not os.path.exists(filepath):
            if len(sort_values) > 0:
                append_data.sort_values(sort_values, inplace=True)
                append_data.reset_index(drop=True, inplace=True)
            append_data.to_feather(filepath)
            logger.debug(f"just created file [{filepath}]...")
        else:
            data = pd.read_feather(filepath)
            data = pd.concat([data, append_data])
            append_data.reset_index(inplace=True)
            if len(drop_duplicates) > 0:
                data.drop_duplicates(drop_duplicates, inplace=True)
            if len(sort_values) > 0:
                data.sort_values(sort_values, inplace=True)
            data.reset_index(drop=True, inplace=True)
            data.to_feather(filepath)
            logger.debug(f"[{filepath}] already exist, update data done, file_data.shape=[{data.shape}]...")

        logger.info(f"append DataFrame to file [{filepath}] Done. sort_values=[{sort_values}], drop_duplicates=[{drop_duplicates}], append_data.shape=[{append_data.shape}]")


    # 文件读取pkl格式DataFrame对象
    @staticmethod
    def loadDataFrameFromPklFile(file_name, folder_abs_path=None):
        folder_abs_path = folder_abs_path if folder_abs_path else PandasConfig.APP_DATA_PATH()
        filepath = os.path.join(folder_abs_path, file_name)
        return pd.read_feather(filepath)