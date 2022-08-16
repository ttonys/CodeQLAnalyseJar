import os
import sys
import time
import logging


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class Logger:
    def __init__(self, logfile=None):
        self.logger = logging.getLogger()
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        if logfile is None:
            cur_path = os.path.split(os.path.realpath(__file__))[0]
            start_time = time.strftime("%Y-%m-%d", time.localtime())
            logfile = cur_path + os.sep + "log_" + start_time + ".log"
        else:
            logfile = logfile
        self.sh = logging.StreamHandler(sys.stdout)
        self.sh.setFormatter(formatter)
        self.logger.addHandler(self.sh)
        # 是否保存log到文件
        # self.fh = logging.FileHandler(logfile)
        # self.fh.setFormatter(formatter)
        # self.logger.addHandler(self.fh)
        self.logger.setLevel(logging.DEBUG)


log = Logger().logger
