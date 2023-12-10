
import os

class BaseConfig:
    # 项目根目录
    APP_ROOT_PATH = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep + '..')

    # 项目data目录
    APP_DATA_FOLDER = './data'
    # APP_DATA_PATH = os.path.join(APP_ROOT_PATH, APP_DATA_FOLDER)

    @classmethod
    def APP_DATA_PATH(cls):
        # TODO
        return os.path.join(BaseConfig.APP_ROOT_PATH, BaseConfig.APP_DATA_FOLDER)
