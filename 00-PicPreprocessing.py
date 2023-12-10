
import os
import logging

from PIL import Image

from conf.config import utils_config_init, AppConfig
from python_library.utils.logUtils import LogUtils


# 配置初始化
utils_config_init()
# 日志句柄
logger = logging.getLogger()
# LogUtils
LogUtils.init_log(log_name='bwiki_illustrated_book-00-PicPreprocessing', console_log='INFO')



# img = Image.open("./data/cut/thor.jpg")
# print(img.size)
# cropped = img.crop((0, 0, 512, 128))  # (left, upper, right, lower)
# cropped.save("./data/cut/pil_cut_thor.jpg")


if __name__ == '__main__':
    oriPath = AppConfig.ToDataAbsPath('./金色ori')
    newPath = AppConfig.ToDataAbsPath('./金色')
    if not os.path.exists(newPath): os.mkdir(newPath)

    for file in os.listdir(oriPath):
        print(file)
        if file == '.DS_Store': continue
        image = Image.open(os.path.join(oriPath, file))
        print(image.size)
        # cropped = image.crop((1787, 734, 4920-1787, 3060-864))
        right = lower = 0
        left = image.size[0]
        upper = image.size[1]
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                if sum(image.getpixel((x, y))) > 10:
                    left = min(left, x)
                    right = max(right, x)
                    upper = min(upper, y)
                    lower = max(lower, y)
        # print(left, upper, right, lower)
        cropped = image.crop((left, upper, right, lower))

        # cropped.show()
        print(os.path.join(newPath, file))
        cropped.save(os.path.join(newPath, file))
