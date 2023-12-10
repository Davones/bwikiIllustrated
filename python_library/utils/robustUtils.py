
import logging, time

from python_library.utils.baseconfig import BaseConfig

logger = logging.getLogger()


class RobustConfig(BaseConfig):
    TRY_TIMES       = 5     # 重试次数
    SLEEP_SECONDS   = 20    # 重试间隔
    # TODO: 重试次数超限告警


class RobustUtils:

    @staticmethod
    def runFunctionTillSuccess(function, tryTimes, sleepTimes):
        '''
        将函数function尝试运行tryTimes次,直到成功返回函数结果和运行次数,否则抛出最后一次失败异常
        '''
        triedTimes = 0
        while True:
            try:
                triedTimes += 1
                result = function()
                return result, triedTimes
            except (Exception) as reason:
                logger.error(f'runFunctionTillSuccess failed ({triedTimes}/{tryTimes}): {reason}')

                # 重试次数超限, 抛出最后一次失败异常
                # TODO: ALARM
                if triedTimes >= tryTimes: raise reason

                if sleepTimes != 0: time.sleep(sleepTimes)  # 一分钟请求20次以内


    def robust(actual_do, *args, **keyargs):
        result, triedTimes = RobustUtils.runFunctionTillSuccess(function=lambda: actual_do(*args, **keyargs),
                                                                tryTimes=RobustConfig.TRY_TIMES,
                                                                sleepTimes=RobustConfig.SLEEP_SECONDS)

        if triedTimes > 1:
            logger.warn(f'RobustUtils execute {actual_do} succ after ({triedTimes}/{RobustConfig.TRY_TIMES}) times tried...')
            # TODO: ALARM

        return result

