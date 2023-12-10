import colorlog
import datetime
import logging
from logging import handlers
import os

from python_library.utils.baseconfig import BaseConfig


class LogConfig(BaseConfig):
    # 日志等级
    LOG_LEVEL = "INFO"

    # 日志格式
    CONSOLE_LOG_FORMAT = '%(log_color)s%(asctime)s-[%(process)d]:[%(thread)d]-%(name)s-%(filename)s-[line:%(lineno)d]-%(levelname)s: %(message)s'
    FILE_LOG_FORMAT = '%(asctime)s-[%(process)d]:[%(thread)d]-%(name)s-%(filename)s-[line:%(lineno)d]-%(levelname)s: %(message)s'

    # 日志文件配置
    LOG_FILE_ROTATING_TIME = 'D'    # 间隔的时间单位: S-秒, M-分, H-小时, D-天, W-每星期(interval==0时代表星期一), midnight-每天凌晨
    LOG_FILE_BACKUP_COUNT = 5       # 备份文件的个数

    # 终端输出日志颜色配置
    LOG_COLORS_CONFIG = {
        'DEBUG':    'white',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }


class LogUtils(object):
    LEVEL_RELATIONS = {
        'DEBUG':    logging.DEBUG,
        'INFO':     logging.INFO,
        'WARNING':  logging.WARNING,
        'ERROR':    logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }   #日志级别关系映射

    @staticmethod
    def init_log(log_name, log_id='', log_level=None, log_folder_name='log', console_log='ERROR'):

        log_level = log_level if log_level is not None else LogConfig.LOG_LEVEL

        # 日志及文件夹路径
        LOG_FLODER_ABS_PATH = os.path.join(LogConfig.APP_ROOT_PATH, log_folder_name)
        LOG_FILE_NAME_ALL = os.path.join(LOG_FLODER_ABS_PATH, '{}-all-{}.log'.format(log_name, datetime.datetime.now().strftime("%Y%m%d")))
        LOG_FILE_NAME_ERROR = os.path.join(LOG_FLODER_ABS_PATH, '{}-error-{}.log'.format(log_name, datetime.datetime.now().strftime("%Y%m%d")))
        if not os.path.exists(LOG_FLODER_ABS_PATH): os.mkdir(LOG_FLODER_ABS_PATH)

        # 初始化logger, 设置默认日志等级
        logger = logging.getLogger(log_id)
        logger.setLevel(logging.DEBUG)


        # 控制台日志
        console_handle = colorlog.StreamHandler()
        console_formatter = colorlog.ColoredFormatter(LogConfig.CONSOLE_LOG_FORMAT, log_colors=LogConfig.LOG_COLORS_CONFIG)
        console_handle.setFormatter(console_formatter)
        console_handle.setLevel(LogUtils.LEVEL_RELATIONS.get(console_log))  # TODO
        logger.addHandler(console_handle)


        # 文件日志 - all
        all_logger_handler = handlers.TimedRotatingFileHandler(filename=LOG_FILE_NAME_ALL, when=LogConfig.LOG_FILE_ROTATING_TIME, backupCount=LogConfig.LOG_FILE_BACKUP_COUNT, encoding='utf-8') #往文件里写入#指定间隔时间自动生成文件的处理器
        all_logger_formatter = logging.Formatter(LogConfig.FILE_LOG_FORMAT, datefmt='%a, %d %b %Y %H:%M:%S')
        all_logger_handler.setFormatter(all_logger_formatter)
        all_logger_handler.setLevel(LogUtils.LEVEL_RELATIONS.get(log_level))
        logger.addHandler(all_logger_handler)


        # 文件日志 - error
        error_logger_handler = handlers.TimedRotatingFileHandler(filename=LOG_FILE_NAME_ERROR, when=LogConfig.LOG_FILE_ROTATING_TIME, backupCount=LogConfig.LOG_FILE_BACKUP_COUNT, encoding='utf-8') #往文件里写入#指定间隔时间自动生成文件的处理器
        error_logger_formatter = logging.Formatter(LogConfig.FILE_LOG_FORMAT, datefmt='%a, %d %b %Y %H:%M:%S')
        error_logger_handler.setFormatter(error_logger_formatter)
        error_logger_handler.setLevel(logging.ERROR)
        logger.addHandler(error_logger_handler)


        # #实例化TimedRotatingFileHandler
        # #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # # S 秒
        # # M 分
        # # H 小时、
        # # D 天、
        # # W 每星期（interval==0时代表星期一）
        # # midnight 每天凌晨

        # 关闭
        # logger.removeHandler(all_logger_handler)
        # all_logger_handler.close()

