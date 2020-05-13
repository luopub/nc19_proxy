import logging.config   # config 配置
import os
from django.conf import settings

# Code learnt from https://www.cnblogs.com/Agoni-7/p/11129296.html

# 定义三种日志输出格式
# 其中name为getlogger指定的名字
standard_format = '[%(asctime)s][%(threadName)s:%(process)d-%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'

logfile_path_staff = os.path.join(settings.BASE_DIR, 'loggings', 'log1.log')

# log配置字典
# LOGGING_DIC第一层的所有的键不能改变
LOGGING_DICT = {
    'version': 1,  # 版本号
    'disable_existing_loggers': False,  #　固定写法
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
    },
    'filters': {},
    'handlers': {
        #打印到终端的日志
        'sh': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'
        },
        #打印到文件的日志,收集info及以上的日志
        'fh': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',
            'filename': logfile_path_staff,  # 日志文件
            'maxBytes': int(1e6),  # 日志大小 n字节
            'backupCount': 5,  # 轮转文件的个数
            'encoding': 'utf-8',  # 日志文件的编码
        },
    },
    'loggers': {
        #logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['sh', 'fh'],  # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}

def get_logger(name):
    logging.config.dictConfig(LOGGING_DICT)  # 导入上面定义的logging配置 通过字典方式去配置这个日志
    logger = logging.getLogger(name)  # 生成一个log实例  这里可以有参数 传给task_id
    return logger
