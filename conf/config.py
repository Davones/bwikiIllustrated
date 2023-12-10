
import os
import re

import python_library.utils.baseconfig
import python_library.utils.logUtils
import python_library.utils.pandasUtils


class AppConfig(python_library.utils.baseconfig.BaseConfig):
    # 图片配置
    PATH_BLACK_LIST_RE = ['.*?.DS_Store', '.*?.xlsx']

    # OCR配置
    OCR_MAX_WORKERS = 8
    OCR_MONITOR_INTERVAL = 1

    @classmethod
    def ToDataAbsPath(cls, subjectPathRe: str):
        return os.path.join(cls.APP_DATA_PATH(), subjectPathRe)

    @classmethod
    def FileMatchBlackList(cls, path: str):
        for pattern in cls.PATH_BLACK_LIST_RE:
            if re.match(pattern, path, flags=0):
                return True
        return False



def utils_config_init():
    # 基础配置 - 项目根路径
    python_library.utils.logUtils.BaseConfig.APP_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + '..')

    # 日志utils
    python_library.utils.logUtils.LogConfig.LOG_LEVEL = "DEBUG"

    # pandas 库配置
    python_library.utils.pandasUtils.PandasUtils.pandas_config_init()

    # ssl全局取消证书验证
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context


utils_config_init()